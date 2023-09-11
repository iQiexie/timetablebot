from sqlalchemy import distinct
from sqlalchemy import func
from sqlalchemy import select

from app.backend.core.repo import BaseRepo
from app.backend.db.models.action import UserActionModel
from app.backend.db.models.user import ExternalUserModel


class StatisticsRepo(BaseRepo[ExternalUserModel]):
    model = ExternalUserModel

    async def get_daily_user_count(self) -> list[dict]:
        stmt = (
            select(
                func.date(UserActionModel.created_at).label("day"),
                func.count(distinct(ExternalUserModel.id)).label("count"),
            )
            .select_from(UserActionModel)
            .join(ExternalUserModel, ExternalUserModel.id == UserActionModel.user_id)
            .group_by(func.date(UserActionModel.created_at))
            .order_by(func.date(UserActionModel.created_at))
        )

        query = await self.session.execute(stmt)
        return query.mappings().all()
