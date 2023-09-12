import logging
import traceback
from contextlib import asynccontextmanager
from typing import (
    Any,
    AsyncContextManager,
    Callable,
    Generic,
    List,
    Optional,
    Sequence,
    TypeVar,
)
from uuid import UUID

from fastapi import Depends
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.exceptions.decorators import expect_arguments
from app.backend.db.base_model import Base
from app.backend.db.dependencies import get_session

ActualModel = TypeVar("ActualModel", bound=Base)
BaseModel = TypeVar("BaseModel", bound=Base)
Model = TypeVar("Model", Base, Base)


class BaseRepo(Generic[ActualModel]):
    model: ActualModel = NotImplemented

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    @asynccontextmanager
    async def transaction(self) -> AsyncContextManager[AsyncSession]:
        try:
            yield self.session
        except Exception as e:
            logging.error(f"Exception occurred in transaction: {e}")
            traceback.print_exc()
            await self.session.rollback()
            raise e

        await self.session.commit()

    async def _base_get(
        self,
        custom_model: BaseModel = None,
        options: list[Callable] = None,
        **kwargs,
    ) -> Any:
        model = custom_model or self.model
        if kwargs:
            stmt = select(model).filter_by(**kwargs)
        else:
            stmt = select(model)

        if options:
            stmt.options(*options)

        return await self.session.execute(stmt)

    @expect_arguments
    async def base_get_one(self, *args, **kwargs) -> Optional[ActualModel]:
        result = await self._base_get(*args, **kwargs)
        return result.scalar_one_or_none()

    @expect_arguments
    async def base_get_list(self, *args, **kwargs) -> Sequence[ActualModel]:
        result = await self._base_get(*args, **kwargs)
        return result.scalars().all()

    async def base_get_all(self, *args, **kwargs) -> Sequence[ActualModel] | List[ActualModel]:
        result = await self._base_get(*args, **kwargs)
        return result.scalars().all()

    async def base_delete_one(self, id_: int | UUID) -> None:
        stmt = delete(self.model).where(self.model.id == id_)
        await self.session.execute(stmt)

    async def base_create(self, **kwargs) -> ActualModel:
        model = self.model(**kwargs)  # noqa
        self.session.add(model)
        return model

    async def base_update(self, model: Generic[BaseModel], *args: Any, **kwargs: Any) -> Model:
        stmt = update(model).where(*args).values(**kwargs).returning(model)
        stmt = select(model).from_statement(stmt).execution_options(synchronize_session="fetch")

        query = await self.session.execute(stmt)
        return query.scalar_one()
