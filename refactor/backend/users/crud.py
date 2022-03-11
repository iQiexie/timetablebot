from sqlalchemy.ext.asyncio import AsyncSession
from refactor.backend.base.crud import BaseCRUD
from refactor.backend.users.models import User, UserMessage
from refactor.backend.users.schemas import UserSchema, UserMessageSchema


class UserCRUD:
    def __init__(self, db_session: AsyncSession):
        self.model = User
        self.schema = UserSchema

        self.base = BaseCRUD(db_session=db_session, model=self.model, schema=self.schema)
        self.message_crud = BaseCRUD(db_session=db_session, model=UserMessage, schema=UserMessageSchema)

    async def log_message(self, **kwargs):
        async with self.message_crud.transaction():
            await self.message_crud.insert(**kwargs)

    async def create(self, **kwargs):
        async with self.base.transaction():
            return await self.base.insert(**kwargs)

    async def get(self, service_name: str):
        async with self.base.transaction():
            return await self.base.get_one(self.model.service_name == service_name)

    async def update(self, service_name: str, **kwargs):
        async with self.base.transaction():
            return await self.base.update(self.model.service_name == service_name, **kwargs)

    async def delete(self, service_name: str):
        async with self.base.transaction():
            return await self.base.delete(self.model.service_name == service_name)