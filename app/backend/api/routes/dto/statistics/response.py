from datetime import date

from pydantic import BaseModel


class DailyUsersResponse(BaseModel):
    day: date
    count: int


class ByGradeResponse(BaseModel):
    grade: int
    count: int
