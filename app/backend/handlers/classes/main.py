from typing import List
from typing import Optional

from app.backend.handlers.classes.enums import ClassesEnum
from app.backend.handlers.classes.enums import LinePositionEnum
from app.backend.handlers.classes.enums import WeekDaysEnum
from app.backend.handlers.classes.redis import ClassesREDIS
from app.backend.handlers.classes.schemes import DaySchema
from app.backend.handlers.classes.scraper import scrape_spreadsheet
from app.backend.redis.utils import compose_key


def get_week_line_position(week_index: int) -> LinePositionEnum:
    if week_index % 2 != 0:
        return LinePositionEnum.ABOVE

    return LinePositionEnum.BELOW


async def get_last_updated() -> str:
    classes_redis = ClassesREDIS()
    return await classes_redis.get("last_updated")


async def update_classes():
    classes_redis = ClassesREDIS()
    classes = await scrape_spreadsheet()
    await classes_redis.replace_classes(classes=classes)


async def find_day(
    group_number: str,
    week_day: Optional[WeekDaysEnum] = None,
    line_position: Optional[LinePositionEnum] = None,
    searching_class: Optional[ClassesEnum] = None,
) -> DaySchema:
    """searching_class returns whole DayScheme with only the required searching_class"""

    if not group_number.isdigit():
        raise AttributeError(f"group_number is not number: {group_number=}")

    classes_redis = ClassesREDIS()

    if not week_day and (line_position or searching_class):
        raise ValueError("week_day must be specified")

    if not line_position and searching_class:
        raise ValueError("line_position must be specified")

    keys = [group_number, week_day, line_position, searching_class]
    classes_query = compose_key(*filter(None, keys))
    result = await classes_redis.get_partial_match(classes_query)

    if not result:
        return DaySchema()

    return DaySchema(**result)


async def find_week(group_number: str, line_position: LinePositionEnum) -> List[DaySchema]:
    days = []

    for week_day in WeekDaysEnum:
        day = await find_day(
            group_number=group_number,
            week_day=week_day,  # noqa
            line_position=line_position,
        )
        days.append(day)

    return days


"""
Examples:
1. Query week

res = await find_week(group_number='317', line_position=LinePositionEnum.BELOW)
    for index, day in enumerate(res):
        print(f'{index + 1}: {day}')
        
        
2. Query specific day
res = await find_day(
    group_number='318',
    week_day=WeekDaysEnum.THURSDAY,
    line_position=LinePositionEnum.ABOVE,
)

"""
