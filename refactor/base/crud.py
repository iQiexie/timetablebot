from contextlib import asynccontextmanager
from typing import Union, ClassVar, Type, TypeVar, AsyncContextManager, cast, Any, List, Callable

from pydantic import BaseModel
from sqlalchemy import update, lambda_stmt, select, delete
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import Executable

from refactor.base.decorators import pydantic_converter
from refactor.base.schema import BaseSchema

Model = TypeVar("Model")
TransactionContext = AsyncContextManager[AsyncSessionTransaction]


class BaseCRUD:
    def __init__(
        self, db_session: Union[sessionmaker, AsyncSession],
        model: ClassVar[Type[Model]],
        schema: Any
    ):
        self.model = model
        self.schema = schema

        if isinstance(db_session, sessionmaker):
            self.session: AsyncSession = cast(AsyncSession, db_session())
        else:
            self.session = db_session

    @asynccontextmanager
    async def transaction(self) -> TransactionContext:
        async with self.session as transaction:
            yield transaction

    async def insert(self, **kwargs: Any) -> Model:
        add_model = self.model(**kwargs)
        self.session.add(add_model)
        await self.session.commit()
        return add_model

    @pydantic_converter
    async def get_one(self, *args) -> Union[List[Model], None]:
        stmt = select(self.model).where(*args)
        result_stmt = await self.session.execute(stmt)
        result = result_stmt.scalars().all()
        if len(result) > 0:
            return result[0]
        return None

    @pydantic_converter
    async def get_many(self, *args: Any) -> List[Model]:
        stmt = select(self.model).where(*args)
        result_stmt = await self.session.execute(stmt)
        result = result_stmt.scalars().all()
        return result

    async def update(self, *args: Any, **kwargs: Any) -> Model:
        res = await self._update(*args, **kwargs)
        return res.scalar_one()

    async def update_many(self, *args: Any, **kwargs: Any) -> Model:
        res = await self._update(*args, **kwargs)
        return res.scalars().all()

    @pydantic_converter
    async def delete(self, *args: Any) -> Result:
        stmt = delete(self.model).where(*args).returning("*")
        result = await self.session.execute(stmt)
        await self.session.commit()

        return result

    @pydantic_converter
    async def _update(self, *args: Any, **kwargs: Any) -> Model:
        stmt = (update(self.model).where(*args).values(**kwargs).returning(self.model))
        stmt = (select(self.model).from_statement(stmt).execution_options(synchronize_session="fetch"))

        result = await self.session.execute(stmt)
        await self.session.commit()
        return result
