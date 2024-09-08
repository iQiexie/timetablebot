import logging
import traceback
from datetime import datetime
from datetime import timedelta
from typing import List
from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.api.routes.dto.classes.request import DayRequest
from app.backend.api.routes.dto.classes.request import DayRequestPattern
from app.backend.api.routes.dto.classes.response import ClassScheme
from app.backend.api.services.classes_scraper import scrape_spreadsheet
from app.backend.api.services.dto.classes import DURATIONS_MAP_FOR_SORTING
from app.backend.api.services.dto.classes import LinePositionEnum
from app.backend.api.services.dto.classes import WEEK_DAYS_NUMBERED
from app.backend.api.services.dto.classes import WeekDaysEnum
from app.backend.api.services.dto.classes_scraper import ScraperResult
from app.backend.core.constants import GRADE_RANGE
from app.backend.core.schemes import SuccessResponse
from app.backend.core.service import ServiceMediator
from app.backend.db.dependencies import get_session
from app.backend.db.models.classes import ClassModel
from app.backend.db.models.user import UserModel
from app.backend.db.repos.classes import ClassesRepo
from app.backend.db.repos.credentials import CredentialsRepo
from app.backend.libs.dto.sheets import Sheet
from app.backend.libs.sheets.client import GoogleAPI


class ClassesService:
    google_api = NotImplementedError

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.services = ServiceMediator(session=session)
        self.google_api = GoogleAPI(repo=CredentialsRepo(session=session))
        self.repo = ClassesRepo(session=session)

    async def get_last_update_time(self) -> datetime:
        async with self.repo.transaction():
            first_class = await self.repo.get_first_class()
            return first_class.updated_at

    @staticmethod
    def get_requested_date(week_day: WeekDaysEnum | str, next_week: bool) -> datetime:
        current_week_day = datetime.now().isocalendar().weekday
        week_days_map = {value: key for key, value in WEEK_DAYS_NUMBERED.items()}
        week_day = week_days_map[week_day]

        if week_day == current_week_day:
            delta = 0
        else:
            delta = week_day - current_week_day

        searching_date = datetime.now() + timedelta(days=delta)

        if next_week:
            searching_date += timedelta(days=7)

        return searching_date

    @staticmethod
    def _cast_classes(classes: List[ClassModel], requested_date: datetime) -> List[ClassScheme]:
        result = [
            ClassScheme(
                id=i.id,
                duration=i.duration,
                value=i.value,
                group_number=i.group_number,
                requested_date=requested_date.date(),
            )
            for i in classes
        ]
        return sorted(result, key=lambda x: DURATIONS_MAP_FOR_SORTING[x.duration])

    async def get_day(
        self,
        week_day: WeekDaysEnum,
        line_position: LinePositionEnum,
        next_week: bool,
        user_id: int,
        current_user: UserModel,
        is_webapp: bool,
    ) -> List[ClassScheme]:
        async with self.repo.transaction():
            user = await self.services.external_user.repo.get_external_user_by_id(
                external_user_id=user_id,
            )

        cords = DayRequest(
            group_number=user.group_number,
            week_day=week_day,
            line_position=line_position,
            next_week=next_week,
        )

        requested_date = self.get_requested_date(
            week_day=cords.week_day,
            next_week=cords.next_week,
        )

        try:
            await self.services.action.mark_action_search(
                user=user,
                day=cords,
                requested_date=requested_date,
                current_user=current_user,
                is_webapp=is_webapp,
            )
        except Exception as e:
            logging.error(f"Cannot mark user activity, because of: {e}")
            traceback.print_exc()

        async with self.repo.transaction():
            classes = await self.repo.get_day(data=cords)
            return self._cast_classes(classes=classes, requested_date=requested_date)

    async def get_day_by_pattern(
        self,
        data: DayRequestPattern,
        current_user: UserModel,
        is_webapp: bool,
    ) -> List[ClassScheme]:
        requested_date = self.get_requested_date(
            week_day=data.week_day,
            next_week=data.next_week,
        )

        try:
            await self.services.action.mark_action_search_pattern(
                user_id=data.user_id,
                requested_date=requested_date,
                pattern=data.pattern,
                current_user=current_user,
                is_webapp=is_webapp,
            )
        except Exception as e:
            logging.error(f"Cannot mark user activity, because of: {e}")
            traceback.print_exc()

        async with self.repo.transaction():
            classes = await self.repo.get_day_by_pattern(
                line_position=data.line_position,
                week_day=data.week_day,
                pattern=data.pattern,
            )
            return self._cast_classes(classes=classes, requested_date=requested_date)

    async def _get_sheets(self) -> dict[int, Sheet]:
        async with self.google_api.repo.transaction() as t:
            await self.google_api.init_services()
            await t.commit()

        sheets = dict()

        for grade, range_str in GRADE_RANGE:
            sheets[grade] = await self.google_api.read_sheet(range_str)

        return sheets

    async def _get_classes(self) -> List[ScraperResult]:
        logging.info("Loading sheets")
        sheets = await self._get_sheets()

        logging.info("Parsing sheets")
        result = scrape_spreadsheet(sheets)

        logging.info("Soring results")
        return sorted(result, key=lambda x: x.group_number)

    async def update_classes(self) -> SuccessResponse:
        classes = await self._get_classes()

        async with self.repo.transaction() as t:
            await self.repo.update_classes(classes=classes)
            await t.commit()

        return SuccessResponse(success=True)

    async def get_class_by_id(self, class_id: int) -> Optional[ClassModel]:
        async with self.repo.transaction():
            return await self.repo.base_get_one(id=class_id)
