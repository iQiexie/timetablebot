from typing import List

from fastapi import APIRouter, Depends, Query

from app.backend.api.dependencies.auth import get_current_user
from app.backend.api.routes.dto.statistics.response import (
    ByGradeResponse,
    DailyUsersResponse,
)
from app.backend.api.services.statistics import StatisticsService
from app.backend.db.models.user import UserModel

statistics_router = APIRouter()


@statistics_router.get(
    path="/statistics/daily",
    response_model=List[DailyUsersResponse],
)
async def get_daily_users(
    user_id: int = Query(...),
    service: StatisticsService = Depends(StatisticsService),
    current_user: UserModel = Depends(get_current_user),
) -> list[dict]:
    return await service.get_daily_user_count(user_id=user_id, current_user=current_user)


@statistics_router.get(
    path="/statistics/total/grade",
    response_model=List[ByGradeResponse],
)
async def get_total_users_graded(
    user_id: int = Query(...),
    service: StatisticsService = Depends(StatisticsService),
    current_user: UserModel = Depends(get_current_user),
) -> list[dict]:
    pass
