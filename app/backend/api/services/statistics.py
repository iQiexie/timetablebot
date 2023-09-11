from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.service import ServiceMediator
from app.backend.db.dependencies import get_session
from app.backend.db.models.action import ButtonsEnum
from app.backend.db.models.user import UserModel
from app.backend.db.repos.statistics import StatisticsRepo


class StatisticsService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.services = ServiceMediator(session=session)
        self.repo = StatisticsRepo(session=session)

    async def get_daily_user_count(self, user_id: int, current_user: UserModel) -> list[dict]:
        async with self.repo.transaction():
            result = await self.repo.get_daily_user_count()

        await self.services.action.mark_action_button_clicked(
            button=ButtonsEnum.statistics_daily_users,
            user_id=user_id,
            current_user=current_user,
        )

        return result
