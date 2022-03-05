from contextlib import asynccontextmanager
from typing import Union, ClassVar, Type, TypeVar, AsyncContextManager, cast, Any

from sqlalchemy import update, lambda_stmt, select, delete
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import Executable

Model = TypeVar("Model")
TransactionContext = AsyncContextManager[AsyncSessionTransaction]


class BaseCRUD:
    def __init__(self, db_session: Union[sessionmaker, AsyncSession], model: ClassVar[Type[Model]]):
        self.model = model

        if isinstance(db_session, sessionmaker):
            self.session: AsyncSession = cast(AsyncSession, db_session())
        else:
            self.session = db_session

    @asynccontextmanager
    async def transaction(self) -> TransactionContext:
        async with self.session as transaction:
            yield transaction

    async def insert(self, **kwargs: Any) -> Model:
        add_model = self._convert_to_model(**kwargs)
        self.session.add(add_model)
        await self.session.commit()
        return add_model

    async def get_one(self, *args) -> Model:
        stmt = select(self.model).where(*args)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_many(self, *args: Any) -> Model:
        query_model = self.model
        stmt = lambda_stmt(lambda: select(query_model))
        stmt += lambda s: s.where(*args)
        query_stmt = cast(Executable, stmt)

        result = await self.session.execute(query_stmt)
        return result.scalars().all()

    async def update(self, *args: Any, **kwargs: Any) -> Model:
        res = await self._update(*args, **kwargs)
        return res.scalar_one()

    async def update_many(self, *args: Any, **kwargs: Any) -> Model:
        res = await self._update(*args, **kwargs)
        return res.scalars().all()

    async def delete(self, *args: Any) -> Result:
        stmt = delete(self.model).where(*args).returning("*")
        result = await self.session.execute(stmt)
        await self.session.commit()

        return result

    async def _update(self, *args: Any, **kwargs: Any) -> Model:
        stmt = (update(self.model).where(*args).values(**kwargs).returning(self.model))
        stmt = (select(self.model).from_statement(stmt).execution_options(synchronize_session="fetch"))

        result = await self.session.execute(stmt)
        await self.session.commit()
        return result

    def _convert_to_model(self, **kwargs) -> Model:
        return self.model(**kwargs)
