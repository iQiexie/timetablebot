from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.backend.api.services.dto.classes import LinePositionEnum
from app.backend.api.services.dto.classes import WeekDaysEnum


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
    telegram_id: Optional[int]
    vk_id: Optional[int]


class RateRequest(BaseModel):
    date: datetime
    correct: bool
    telegram_id: Optional[int]
    vk_id: Optional[int]
    pattern: Optional[str]
