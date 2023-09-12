from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, Query

from app.backend.api.dependencies.auth import get_current_user
from app.backend.api.routes.dto.classes.request import DayRequestPattern, RateRequest
from app.backend.api.routes.dto.classes.response import ClassScheme
from app.backend.api.services.action import ActionService
from app.backend.api.services.classes import ClassesService
from app.backend.api.services.dto.classes import LinePositionEnum, WeekDaysEnum
from app.backend.core.schemes import SuccessResponse
from app.backend.db.models.user import UserModel

classes_router = APIRouter()


@classes_router.patch(
    path="/classes",
    response_model=SuccessResponse,
)
async def update_classes(
    service: ClassesService = Depends(ClassesService),
    _: UserModel = Depends(get_current_user),
) -> SuccessResponse:
    return await service.update_classes()


@classes_router.get(
    path="/classes/days",
    response_model=List[ClassScheme],
)
async def get_classes_for_day(
    week_day: WeekDaysEnum = Query(...),
    line_position: LinePositionEnum = Query(...),
    next_week: bool = Query(...),
    user_id: int = Query(...),
    service: ClassesService = Depends(ClassesService),
    current_user: UserModel = Depends(get_current_user),
) -> List[ClassScheme]:
    return await service.get_day(
        week_day=week_day,
        line_position=line_position,
        user_id=user_id,
        next_week=next_week,
        current_user=current_user,
    )


@classes_router.get(
    path="/classes/pattern",
    response_model=List[ClassScheme],
)
async def get_classes_by_pattern(
    pattern: str = Query(...),
    week_day: WeekDaysEnum = Query(...),
    line_position: LinePositionEnum = Query(...),
    next_week: bool = Query(...),
    user_id: int = Query(...),
    service: ClassesService = Depends(ClassesService),
    current_user: UserModel = Depends(get_current_user),
) -> List[ClassScheme]:
    return await service.get_day_by_pattern(
        current_user=current_user,
        data=DayRequestPattern(
            pattern=pattern,
            week_day=week_day,
            line_position=line_position,
            next_week=next_week,
            user_id=user_id,
            current_user=current_user,
        ),
    )


@classes_router.post(
    path="/classes/rate",
    response_model=SuccessResponse,
)
async def rate_response(
    data: RateRequest,
    action_service: ActionService = Depends(ActionService),
    current_user: UserModel = Depends(get_current_user),
) -> SuccessResponse:
    await action_service.mark_action_rate(data=data, current_user=current_user)
    return SuccessResponse(success=True)


@classes_router.get(
    path="/classes/last_update",
    response_model=dict[str, datetime],
)
async def get_last_updated_at(
    service: ClassesService = Depends(ClassesService),
) -> dict[str, datetime]:
    result = await service.get_last_update_time()
    return {"last_update": result}
