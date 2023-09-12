import math
from datetime import datetime
from typing import List

from sqlalchemy import and_, select
from sqlalchemy.dialects.postgresql import insert

from app.backend.api.routes.dto.classes.request import DayRequest
from app.backend.api.services.dto.classes import LinePositionEnum, WeekDaysEnum
from app.backend.api.services.dto.classes_scraper import ScraperResult
from app.backend.core.repo import BaseRepo
from app.backend.db.models.classes import ClassModel


class ClassesRepo(BaseRepo[ClassModel]):
    model = ClassModel

    async def get_first_class(self) -> ClassModel:
        stmt = select(self.model).order_by(self.model.id).limit(1)
        query = await self.session.execute(stmt)
        return query.scalar()

    async def get_day(self, data: DayRequest) -> List[ClassModel]:
        stmt = select(self.model).where(
            and_(
                self.model.line_position == data.line_position,
                self.model.group_number == data.group_number,
                self.model.week_day == data.week_day,
            )
        )

        query = await self.session.execute(stmt)
        return query.scalars().all()

    async def get_day_by_pattern(
        self,
        line_position: LinePositionEnum,
        week_day: WeekDaysEnum,
        pattern: str,
    ) -> List[ClassModel]:
        stmt = select(self.model).where(
            and_(
                self.model.line_position == line_position,
                self.model.value.ilike(f"%{pattern.lower()}%"),
                self.model.week_day == week_day,
            )
        )

        query = await self.session.execute(stmt)
        return query.scalars().all()

    async def update_classes(self, classes: List[ScraperResult]) -> None:
        await self.session.execute("truncate classes")

        values = [{**value.dict(), "updated_at": datetime.now()} for value in classes]

        args_per_row = len(values[0])
        psql_query_allowed_max_args = 3000
        allowed_args_per_query = int(math.floor(psql_query_allowed_max_args / args_per_row))
        query_args_sets = [
            values[x : x + allowed_args_per_query] for x in range(0, len(values), allowed_args_per_query)
        ]

        for arg_set in query_args_sets:
            stmt = insert(self.model).values(arg_set)
            stmt = stmt.on_conflict_do_update(
                constraint="classes_group_number_week_day_line_position_duration_row_in_key",
                set_={"value": stmt.excluded.value},
            )

            await self.session.execute(stmt)
