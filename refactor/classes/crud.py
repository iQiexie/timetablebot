from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from refactor.base.crud import BaseCRUD
from refactor.classes.models import Class
from refactor.classes.schemas import ClassSchema


class ClassesCRUD:
    def __init__(self, db_session: AsyncSession):
        self.model = Class
        self.schema = ClassSchema
        self.base = BaseCRUD(db_session=db_session, model=self.model, schema=self.schema)

    async def create(self, **kwargs):
        async with self.base.transaction():
            return await self.base.insert(**kwargs)

    async def get(self, group_id: int, absolute_index: int):
        async with self.base.transaction():
            return await self.base.get_many(and_(
                self.model.group_id == group_id,
                self.model.absolute_index == absolute_index
            ))

    async def update(self, group_id: int, absolute_index: int, **kwargs):
        async with self.base.transaction():
            return await self.base.update(
                and_(self.model.group_id == group_id, self.model.absolute_index == absolute_index),
                **kwargs
            )

    async def delete(self, group_id: int, absolute_index: int):
        async with self.base.transaction():
            return await self.base.delete((and_(
                self.model.group_id == group_id,
                self.model.absolute_index == absolute_index
            )))
