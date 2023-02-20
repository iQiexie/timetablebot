from datetime import datetime
from typing import List
from typing import Optional

from sqlalchemy import select
from sqlalchemy import text
from sqlalchemy import update

from app.backend.db.base_crud import BaseCRUD
from app.backend.handlers.users.models import User
from app.backend.handlers.users.models import UsersActivity


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
        sql = update(User).where(User.vk_id == vk_id).values(last_activity=datetime.now())
        await self.session.execute(sql)
        await self.session.commit()

    async def get_daily_users(self) -> int:
        sql = text("SELECT count(*) FROM users WHERE last_activity >= NOW() - INTERVAL '1 day'")
        query = await self.session.execute(sql)
        return query.scalar_one_or_none()

    async def get_daily_users_by_day(self) -> List[UsersActivity]:
        sql = select(UsersActivity)
        query = await self.session.execute(sql)
        return list(query.scalars())

    async def record_daily_users(self):
        count = await self.get_daily_users()
        self.session.add(UsersActivity(user_count=count))
        await self.session.commit()
