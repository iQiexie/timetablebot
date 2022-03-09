from typing import List

from refactor.base.db import async_session
from refactor.base.utils import safe_pop, safe_get
from refactor.classes.crud import ClassesCRUD
from refactor.classes.schemas import ClassSchema, DaySchema, MetaInfoSchema
from refactor.google_api.crud import GoogleApiCRUD
from refactor.google_api.handlers import GoogleApiHandler


async def _get_hyperlink(info: MetaInfoSchema, class_index: int):
    if info.grade == 1:
        hyperlink_index = 7 + class_index
    else:
        hyperlink_index = 12 + class_index

    links = await safe_get(info.hyperlinks, hyperlink_index)
    hyperlinks = []

    try:
        for possible_hyperlink in links['values']:
            hyperlinks.append(possible_hyperlink.get("hyperlink"))
    except (KeyError, AttributeError, TypeError):
        pass

    return hyperlinks


async def _scrape_days(info: MetaInfoSchema, start_week: int) -> List[List[dict]]:
    """  start_week == 0 - над чертой; start_week == 1 - под чертой. """
    classes = []
    for index in range(start_week, len(info.class_column), 2):
        classes.append({
            "class": info.class_column[index],
            "hyperlinks": await _get_hyperlink(info, index)
        })
    day_classes = []
    for i in range(6):
        temp_day = []
        for j in range(5):
            temp_day.append(await safe_pop(classes, 0))
        day_classes.append(temp_day)

    return day_classes


async def scrape_days(info: MetaInfoSchema) -> List[DaySchema]:
    """ парсит целую колонку (всё расписание для одной группы). Возвращает дни """
    days = []
    for i in range(2):
        day_classes = await _scrape_days(info, i)
        for index, day_class in enumerate(day_classes):
            days.append(
                DaySchema(
                    week_day_index=index,
                    above_line=i % 2 == 0,
                    classes=day_class,
                    group_id=info.group_id
                )
            )

    return days


async def scrape_classes(days: List[DaySchema]):
    """ парсит сами пары. Добавляет их в бд """
    classes = []
    for day in days:
        for lesson in day.classes:
            classes.append(ClassSchema(
                week_day_index=day.week_day_index,
                above_line=day.above_line,
                group_id=day.group_id,
                text=lesson.get("class"),
                hyperlinks=lesson.get("hyperlinks")
            ))

    return classes


async def scrape_spreadsheet():
    google = GoogleApiHandler(GoogleApiCRUD(async_session))
    await google.init_services()
    for grade in range(2, 3):
        """ сделать отдельный цикл для grade == 2. Там 210 группы нет """
        lessons, hyperlinks = await google.get_values(grade)
        columns = lessons.get("values")
        for index, column in enumerate(columns):
            print(f"group: {index + 1}")
            days = await scrape_days(MetaInfoSchema(
                class_column=column,
                hyperlinks=hyperlinks,
                grade=grade,
                group_id=index + 1
            ))
            return await scrape_classes(days)
            # last_row_index = ROWS_IN_DAY
            # print(group_index)
            # for week_day_index in range(1, 7):
            #     one_day_rows = column[last_row_index * (week_day_index - 1): last_row_index * week_day_index]
            #     await scrape_day(one_day_rows, week_day_index)
