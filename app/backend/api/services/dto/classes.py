from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.backend.core.schemes import BaseModelORM
from app.backend.core.schemes import StrEnum


class ClassesEnum(str, Enum):
    FIRST_CLASS = "9.00-10.30"
    SECOND_CLASS = "10.40-12.10"
    THIRD_CLASS = "12.40-14.10"
    FOURTH_CLASS = "14.20-16.00"
    FIFTH_CLASS = "16.00-17.30"
    FIFTH_CLASS2 = "17:00-18:30"
    FIFTH_CLASS2_2 = "17.00-18.30"
    SIXTH_CLASS = "18:40-20:10"
    SIXTH_CLASS_2 = "18.40-20.10"


class WeekDaysEnum(str, Enum):
    MONDAY = "ПОНЕДЕЛЬНИК"
    TUESDAY = "ВТОРНИК"
    WEDNESDAY = "СРЕДА"
    THURSDAY = "ЧЕТВЕРГ"
    FRIDAY = "ПЯТНИЦА"
    SATURDAY = "СУББОТА"
    SUNDAY = "ВОСКРЕСЕНЬЕ"


class LinePositionEnum(StrEnum):
    ABOVE = "НАД"
    BELOW = "ПОД"


WEEK_DAYS_NUMBERED = {
    1: WeekDaysEnum.MONDAY,
    2: WeekDaysEnum.TUESDAY,
    3: WeekDaysEnum.WEDNESDAY,
    4: WeekDaysEnum.THURSDAY,
    5: WeekDaysEnum.FRIDAY,
    6: WeekDaysEnum.SATURDAY,
    7: WeekDaysEnum.SUNDAY,
}

DURATIONS_MAP = {
    "9.00-10.30": "first_class",
    "10.40-12.10": "second_class",
    "12.40-14.10": "third_class",
    "14.20-16.00": "fourth_class",
    "16.00-17.30": "fifth_class",
    "17.00-18.30": "fifth_class2",
    "18.40-20.10": "sixth_class",
    "17:00-18:30": "fifth_class2",
    "18:40-20:10": "sixth_class",
    "16.00-17-30": "fifth_class",
}


DURATIONS_MAP_FOR_SORTING = {
    ClassesEnum.FIRST_CLASS: 1,
    ClassesEnum.SECOND_CLASS: 2,
    ClassesEnum.THIRD_CLASS: 3,
    ClassesEnum.FOURTH_CLASS: 4,
    ClassesEnum.FIFTH_CLASS: 5,
    ClassesEnum.FIFTH_CLASS2: 6,
    ClassesEnum.FIFTH_CLASS2_2: 6,
    ClassesEnum.SIXTH_CLASS: 7,
    ClassesEnum.SIXTH_CLASS_2: 7,
}

# в DURATIONS_MAP можно добавлять сколько угодно продолжительностей (вроде 16.00-17.30).
# app.backend.handlers.classes.scraper всё равно потом приводит всё к одному формату:
# 16.00-17.30 (часы.минуты-часы.минуты)
# эти продолжительности ещё используются в app.backend.handlers.classes.enums


class ClassSchema(BaseModelORM):
    value: str
    group: int
    display_group: bool

    def __str__(self):
        if not self.display_group:
            return self.value

        return f"Группа: {self.group}\n\n{self.value}"


class ClassCords(BaseModel):
    group_number: Optional[int]
    week_day: WeekDaysEnum
    line_position: LinePositionEnum
    duration: str
    row_index: int

    _separator = ":"

    class Config:
        use_enum_values = True

    def __str__(self) -> str:
        return self._separator.join(
            (
                self.group_number,
                self.week_day,
                self.line_position,
                self.duration,
                self.row_index,
            )
        )

    @classmethod
    def from_str(cls, data: str) -> "ClassCords":
        group_number, week_day, line_position, duration, row_index = data.split(cls._separator)
        return cls(
            group_number=group_number,
            week_day=week_day,
            line_position=line_position,
            duration=duration,
            row_index=row_index,
        )
