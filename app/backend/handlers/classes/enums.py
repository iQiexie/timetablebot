from enum import Enum


class ClassesEnum(str, Enum):
    FIRST_CLASS = "9.00-10.30"
    SECOND_CLASS = "10.40-12.10"
    THIRD_CLASS = "12.40-14.10"
    FOURTH_CLASS = "14.20-16.00"
    FIFTH_CLASS = "16.00-17.30"
    FIFTH_CLASS2 = "17:00-18:30"
    SIXTH_CLASS = "18:40-20:10"


class WeekDaysEnum(str, Enum):
    MONDAY = "ПОНЕДЕЛЬНИК"
    TUESDAY = "ВТОРНИК"
    WEDNESDAY = "СРЕДА"
    THURSDAY = "ЧЕТВЕРГ"
    FRIDAY = "ПЯТНИЦА"
    SATURDAY = "СУББОТА"
    SUNDAY = "ВОСКРЕСЕНЬЕ"


class LinePositionEnum(str, Enum):
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
