from datetime import datetime
from datetime import timedelta
from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from app.backend.api.dependencies.auth import get_current_user
from app.backend.api.routes.dto.classes.request import DayRequestPattern
from app.backend.api.routes.dto.classes.request import RateRequest
from app.backend.api.routes.dto.classes.response import ClassScheme
from app.backend.api.services.action import ActionService
from app.backend.api.services.classes import ClassesService
from app.backend.api.services.dto.classes import LinePositionEnum
from app.backend.api.services.dto.classes import WeekDaysEnum
from app.backend.core.schemes import SuccessResponse

classes_router = APIRouter()


@classes_router.patch(
    path="/classes",
    response_model=SuccessResponse,
    dependencies=[Depends(get_current_user)],
)
async def update_classes(service: ClassesService = Depends(ClassesService)) -> SuccessResponse:
    return await service.update_classes()


@classes_router.get(
    path="/classes/days",
    response_model=List[ClassScheme],
    dependencies=[Depends(get_current_user)],
)
async def get_classes_for_day(
    week_day: WeekDaysEnum = Query(...),
    line_position: LinePositionEnum = Query(...),
    next_week: bool = Query(...),
    vk_id: Optional[int] = Query(None),
    telegram_id: Optional[int] = Query(None),
    service: ClassesService = Depends(ClassesService),
) -> List[ClassScheme]:
    return await service.get_day(
        week_day=week_day,
        line_position=line_position,
        vk_id=vk_id,
        telegram_id=telegram_id,
        next_week=next_week,
    )


@classes_router.get(
    path="/classes/pattern",
    response_model=List[ClassScheme],
    dependencies=[Depends(get_current_user)],
)
async def get_classes_by_pattern(
    pattern: str = Query(...),
    week_day: WeekDaysEnum = Query(...),
    line_position: LinePositionEnum = Query(...),
    next_week: bool = Query(...),
    telegram_id: Optional[int] = Query(None),
    vk_id: Optional[int] = Query(None),
    service: ClassesService = Depends(ClassesService),
) -> List[ClassScheme]:
    return await service.get_day_by_pattern(
        data=DayRequestPattern(
            pattern=pattern,
            week_day=week_day,
            line_position=line_position,
            next_week=next_week,
            telegram_id=telegram_id,
            vk_id=vk_id,
        )
    )


@classes_router.post(
    path="/classes/rate",
    response_model=SuccessResponse,
    dependencies=[Depends(get_current_user)],
)
async def rate_response(
    data: RateRequest,
    action_service: ActionService = Depends(ActionService),
) -> SuccessResponse:
    await action_service.mark_action_rate(data=data)
    return SuccessResponse(success=True)


@classes_router.get(
    path="/classes/last_update",
    response_model=dict[str, datetime],
)
async def get_last_updated_at(
    service: ClassesService = Depends(ClassesService),
) -> dict[str, datetime]:
    result = await service.get_last_update_time()
    return {"last_update": result + timedelta(hours=3)}
