from typing import List

from app.backend.classes.schemas import ClassSchema, DaySchema, MetaInfoSchema
from app.backend.google_api.handlers import GoogleApiHandler
from app.utils import safe_get, safe_pop


async def _get_hyperlink(info: MetaInfoSchema, class_index: int):
    if info.grade == 1:
        hyperlink_index = 7 + class_index
    else:
        hyperlink_index = 12 + class_index

    links = safe_get(info.hyperlinks, hyperlink_index)
    hyperlinks = []

    try:
        for possible_hyperlink in links['values']:
            hyperlink = possible_hyperlink.get("hyperlink")
            hyperlinks.append(hyperlink) if hyperlink else None

    except (KeyError, AttributeError, TypeError):
        pass

    return hyperlinks


async def _scrape_days(info: MetaInfoSchema, start_week: int) -> List[List[dict]]:
    """  start_week == 0 - над чертой; start_week == 1 - под чертой. """
    classes = []
    for index in range(start_week, len(info.class_column), 2):
        if info.grade == 1 and index > 26 - 7:  # TEMP. УДАЛИТЬ, КОГДА ЗАКОНЧИТСЯ ЗНАКОМСТВО С БИБЛОТЕКОЙ
            index += 1  # TEMP. УДАЛИТЬ, КОГДА ЗАКОНЧИТСЯ ЗНАКОМСТВО С БИБЛОТЕКОЙ

        if index >= len(info.class_column):  # TEMP. УДАЛИТЬ, КОГДА ЗАКОНЧИТСЯ ЗНАКОМСТВО С БИБЛОТЕКОЙ
            continue  # TEMP. УДАЛИТЬ, КОГДА ЗАКОНЧИТСЯ ЗНАКОМСТВО С БИБЛОТЕКОЙ

        classes.append({
            "class": info.class_column[index] + f"\n\nindex: {index}",
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


async def scrape_classes(days: List[DaySchema]) -> List[DaySchema]:
    """ парсит сами пары. Добавляет их в бд """
    better_days = []
    for day in days:
        class_schemas = []

        for index, lesson in enumerate(day.classes):
            if type(lesson) == list:
                lesson = {'class': '', 'hyperlinks': ''}

            class_model = ClassSchema(
                index=index + 1,
                text=lesson.get("class"),
                hyperlinks=lesson.get("hyperlinks")
            )

            class_schemas.append(class_model)

        day.classes = class_schemas
        better_days.append(day)

    return better_days


async def _scrape_spreadsheet(columns: str, hyperlinks: list, grade: int, final_classes: list):
    for index, column in enumerate(columns):
        days = await scrape_days(MetaInfoSchema(
            class_column=column,
            hyperlinks=hyperlinks,
            grade=grade,
            group_id=index + 1 + grade*100
        ))
        for _class in await scrape_classes(days):
            final_classes.append(_class)

    return final_classes


async def parse_5th_grade(columns, hyperlinks, grade, final_classes):
    for i in range(0, len(columns)):
        index = i + 5
        column = columns[i]

        days = await scrape_days(
            MetaInfoSchema(
                class_column=column,
                hyperlinks=hyperlinks,
                grade=grade,
                group_id=index + 1 + grade * 100
            )
        )

        for _class in await scrape_classes(days):
            final_classes.append(_class)

    return final_classes


async def parse_3rd_grade(columns, hyperlinks, grade, final_classes):
    for i in range(len(columns)):
        if i < 10:
            index = i
            column = columns[i]
        else:
            index = i + 1
            column = columns[i]

        days = await scrape_days(
            MetaInfoSchema(
                class_column=column,
                hyperlinks=hyperlinks,
                grade=grade,
                group_id=index + 1 + grade * 100
            )
        )

        for _class in await scrape_classes(days):
            final_classes.append(_class)

    return final_classes


async def scrape_spreadsheet() -> list[DaySchema]:
    google = GoogleApiHandler()
    await google.init_services()

    final_classes = []

    for grade in range(1, 6):
        print(grade)
        result = await google.get_values(grade)

        if result is None:
            return []

        lessons, hyperlinks = result
        columns = lessons.get("values")

        if grade == 5:
            # костыль для 5 курса, где группы начинаются с 506
            final_classes = await parse_5th_grade(columns, hyperlinks, grade, final_classes)
        elif grade == 3:
            # костыль для пропущенного столбика 310 группы
            final_classes = await parse_3rd_grade(columns, hyperlinks, grade, final_classes)
        else:
            final_classes = await _scrape_spreadsheet(columns, hyperlinks, grade, final_classes)

    return final_classes
