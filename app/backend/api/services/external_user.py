from typing import List
from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.api.routes.dto.user.request import ExternalUserCreate
from app.backend.api.routes.dto.user.request import ExternalUserUpdate
from app.backend.core.service import ServiceMediator
from app.backend.db.dependencies import get_session
from app.backend.db.models.user import ExternalUserModel
from app.backend.db.models.user import UserModel
from app.backend.db.repos.external_user import ExternalUserRepo


class ExternalUserService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.services = ServiceMediator(session=session)
        self.repo = ExternalUserRepo(session=session)

    async def get_all_users(self) -> List[ExternalUserModel]:
        async with self.repo.transaction():
            return await self.repo.get_all_users()

    async def get_user_by_external_id(
        self,
        telegram_id: Optional[int] = None,
        vk_id: Optional[int] = None,
    ) -> Optional[ExternalUserModel]:
        async with self.repo.transaction():
            result = await self.repo.get_user_by_external_id(telegram_id=telegram_id, vk_id=vk_id)
            if len(result) < 1:
                return

            user = result[0]["ExternalUserModel"]
            user.gpt_allowed = result[0]["gpt_allowed"]
            return user

    async def create_external_user(self, data: ExternalUserCreate) -> ExternalUserCreate:
        async with self.repo.transaction() as t:
            existing_user = await self.get_user_by_external_id(
                vk_id=data.vk_id,
                telegram_id=data.telegram_id,
            )

            if existing_user:
                existing_user = await self.repo.update_external_user(
                    vk_id=data.vk_id,
                    telegram_id=data.telegram_id,
                    first_name=data.first_name,
                    last_name=data.last_name,
                    username=data.username,
                )
                await t.commit()
                return existing_user

            result = await self.repo.create_external_user(
                telegram_id=data.telegram_id,
                vk_id=data.vk_id,
                group_number=data.group_number,
                first_name=data.first_name,
                last_name=data.last_name,
                username=data.username,
            )

            await t.commit()

        return result

    async def update_external_user(
        self,
        data: ExternalUserUpdate,
        current_user: UserModel,
    ) -> ExternalUserModel:
        await self.services.action.mark_action_settings(
            vk_id=data.vk_id,
            telegram_id=data.telegram_id,
            new_group=data.group_number,
            current_user=current_user,
        )

        async with self.repo.transaction() as t:
            await self.repo.update_external_user(
                vk_id=data.vk_id,
                telegram_id=data.telegram_id,
                group_number=data.group_number,
            )

            result = await self.get_user_by_external_id(
                vk_id=data.vk_id,
                telegram_id=data.telegram_id,
            )
            await t.commit()

        return result
