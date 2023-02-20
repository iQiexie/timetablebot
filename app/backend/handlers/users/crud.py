from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy import update

from app.backend.db.base_crud import BaseCRUD
from app.backend.handlers.users.models import User


class UserCRUD(BaseCRUD[User]):
    async def create(self, vk_id: int) -> User:
        user = User(vk_id=vk_id)  # noqa
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get(self, vk_id: int) -> User:
        stmt = select(User).where(User.vk_id == vk_id)
        query = await self.session.execute(stmt)
        return query.scalar_one_or_none()

    async def user_exists(self, vk_id: int):
        user = await self.get(vk_id)
        return user is None

    async def update_group(self, vk_id: int, group_number: int) -> User:
        stmt = update(User).where(User.vk_id == vk_id).values(group_index=group_number)
        await self.session.execute(stmt)
        await self.session.commit()

        return await self.get(vk_id=vk_id)

    async def mark_last_activity(self, vk_id: str):
        # TODO refactor

        try:
            # sql = f"update users set last_activity = '{datetime.now()}' where vk_id = {vk_id}"
            sql = update(User).where(User.vk_id == vk_id).values(last_activity=datetime.now())
            await self.session.execute(sql)
            await self.session.commit()
        except Exception as e:
            print(f"mark_last_activity failed due to {e=}. {vk_id=}")
