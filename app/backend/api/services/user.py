from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.api.routes.dto.user.request import UserIn
from app.backend.api.services.auth import SecurityService
from app.backend.core.exceptions.decorators import expect_arguments
from app.backend.core.exceptions.http_exceptions import Custom400Exception
from app.backend.core.service import ServiceMediator
from app.backend.db.dependencies import get_session
from app.backend.db.models.user import UserModel
from app.backend.db.repos.user import UserRepo


class UserService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.mediator = ServiceMediator(session=session)
        self.repo = UserRepo(session=session)

    async def create_user(self, data: UserIn) -> UserModel:
        hashed_password = SecurityService().get_password_hash(data.password)

        async with self.repo.transaction() as t:
            data = data.dict()
            data["password"] = hashed_password
            result = await self.repo.create_user(**data)
            await t.commit()

        return result

    @expect_arguments
    async def get_user(self, user_id: int, user_name: str) -> Optional[UserModel]:
        async with self.repo.transaction():
            if user_id:
                result = await self.repo.base_get_one(id=user_id)
            elif user_name:
                result = await self.repo.base_get_one(username=user_name)

        if not result:
            raise Custom400Exception(msg="User is not found")

        return result
