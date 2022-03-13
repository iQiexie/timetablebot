from sqlalchemy.ext.asyncio import AsyncSession
from refactor.backend.base.crud import BaseCRUD
from refactor.backend.base.decorators import pydantic_converter
from refactor.backend.users.models import User, UserMessage
from refactor.backend.users.schemas import UserSchema, UserMessageSchema


class UserCRUD:
    def __init__(self, db_session: AsyncSession):
        self.model = User
        self.schema = UserSchema

        self.base = BaseCRUD(db_session=db_session, model=self.model, schema=self.schema)
        self.message_crud = BaseCRUD(db_session=db_session, model=UserMessage, schema=UserMessageSchema)

    async def log_message(self, **kwargs):
        # TODO перенести в логи

        async with self.message_crud.transaction():
            await self.message_crud.insert(**kwargs)

    async def user_exists(self, vk_id: int):
        user = await self.get(vk_id)
        return user is None

    async def create(self, **kwargs):
        async with self.base.transaction():
            return await self.base.insert(**kwargs)

    @pydantic_converter
    async def get(self, vk_id: int):
        async with self.base.transaction():
            return await self.base.get_one(self.model.vk_id == vk_id)

    async def update(self, vk_id: str, **kwargs):
        async with self.base.transaction():
            return await self.base.update(self.model.vk_id == vk_id, **kwargs)

    async def delete(self, vk_id: str):
        async with self.base.transaction():
            return await self.base.delete(self.model.vk_id == vk_id)
