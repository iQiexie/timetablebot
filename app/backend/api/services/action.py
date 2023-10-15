from datetime import datetime
from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.api.routes.dto.classes.request import DayRequest
from app.backend.api.routes.dto.classes.request import RateRequest
from app.backend.core.service import ServiceMediator
from app.backend.db.dependencies import get_session
from app.backend.db.models.action import ActionsEnum
from app.backend.db.models.action import ButtonsEnum
from app.backend.db.models.user import ExternalUserModel
from app.backend.db.models.user import UserModel
from app.backend.db.repos.user import UserRepo


class ActionService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.services = ServiceMediator(session=session)
        self.repo = UserRepo(session=session)

    async def mark_action_button_clicked(
        self,
        button: ButtonsEnum,
        user_id: int,
        current_user: UserModel,
        pattern: Optional[str] = None,
    ) -> None:
        async with self.repo.transaction() as t:
            existing_user = await self.services.external_user.repo.get_external_user_by_id(
                external_user_id=user_id,
            )

            await self.repo.create_action(
                user_id=existing_user.id,
                action=ActionsEnum.button_clicked,
                button=button,
                created_at=datetime.now(),
                pattern=pattern,
                source=current_user.source,
            )
            await t.commit()

    async def mark_action_search(
        self,
        user: ExternalUserModel,
        day: DayRequest,
        requested_date: datetime,
        current_user: UserModel,
    ) -> None:
        async with self.repo.transaction() as t:
            await self.repo.create_action(
                user_id=user.id,
                action=ActionsEnum.search,
                created_at=datetime.now(),
                requested_day=requested_date.date(),
                new_group=day.group_number,
                current_group=user.group_number,
                source=current_user.source,
            )
            await t.commit()

    async def mark_action_search_pattern(
        self,
        pattern: str,
        requested_date: datetime,
        user_id: int,
        current_user: UserModel,
    ) -> None:
        async with self.repo.transaction() as t:
            user = await self.services.external_user.repo.get_external_user_by_id(
                external_user_id=user_id,
            )

            await self.repo.create_action(
                user_id=user.id,
                action=ActionsEnum.search_pattern,
                created_at=datetime.now(),
                requested_day=requested_date.date(),
                current_group=user.group_number,
                pattern=pattern,
                source=current_user.source,
            )
            await t.commit()

    async def mark_action_settings(
        self,
        new_group: int,
        current_user: UserModel,
        telegram_id: Optional[int] = None,
        vk_id: Optional[int] = None,
    ) -> None:
        async with self.repo.transaction() as t:
            user = await self.services.external_user.get_user_by_external_id(
                telegram_id=telegram_id,
                vk_id=vk_id,
            )

            await self.repo.create_action(
                user_id=user.id,
                created_at=datetime.now(),
                action=ActionsEnum.change_settings,
                current_group=user.group_number,
                new_group=new_group,
                source=current_user.source,
            )
            await t.commit()

    async def mark_action_rate(self, data: RateRequest, current_user: UserModel) -> None:
        user = await self.services.external_user.get_user_by_external_id(
            telegram_id=data.telegram_id,
            vk_id=data.vk_id,
        )

        async with self.repo.transaction() as t:
            await self.repo.create_action(
                user_id=user.id,
                created_at=datetime.now(),
                action=ActionsEnum.rate,
                current_group=user.group_number,
                correct=data.correct,
                requested_day=data.date.date(),
                pattern=data.pattern,
                source=current_user.source,
            )
            await t.commit()
