from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.backend.api.services.dto.classes import LinePositionEnum
from app.backend.api.services.dto.classes import WeekDaysEnum
from app.backend.db.models.user import UserModel


class DayRequest(BaseModel):
    group_number: int
    week_day: WeekDaysEnum
    line_position: LinePositionEnum
    next_week: bool


class DayRequestPattern(BaseModel):
    pattern: str
    week_day: WeekDaysEnum
    line_position: LinePositionEnum
    next_week: bool
    user_id: int
    current_user: UserModel

    class Config:
        arbitrary_types_allowed = True


class RateRequest(BaseModel):
    date: datetime
    correct: bool
    telegram_id: Optional[int]
    vk_id: Optional[int]
    pattern: Optional[str]
