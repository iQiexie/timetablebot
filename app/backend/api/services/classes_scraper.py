import logging
from typing import List

from app.backend.api.services.dto.classes import ClassCords
from app.backend.api.services.dto.classes import DURATIONS_MAP
from app.backend.api.services.dto.classes import LinePositionEnum
from app.backend.api.services.dto.classes import WeekDaysEnum
from app.backend.api.services.dto.classes_scraper import ScraperResult
from app.backend.core.constants import GRADE_RANGE
from app.backend.libs.dto.sheets import Sheet
from app.backend.libs.dto.sheets import SheetValue


def get_column_url(column: SheetValue) -> str:
    for format_runs in column.text_format_runs or []:
        if not format_runs.format.link:
            continue

        if url := format_runs.format.link.uri:
            return url


def scrape_spreadsheet(sheets: dict[int, Sheet]) -> List[ScraperResult]:
    final_classes = []

    for grade in range(*GRADE_RANGE):
        logging.info(f"Parsing grade: {grade}")
        sheet = sheets[grade]

        group_indexes = {}
        week_days = [value for value in WeekDaysEnum]
        durations = DURATIONS_MAP.keys()
        line_positions = [i for i in LinePositionEnum]

        classes = []
        last_week_day = None
        last_duration = None
        last_cords = None

        for row_index, row in enumerate(sheet.row_data):
            if not row.values:
                continue

            for index, column in enumerate(row.values):
                column_value = column.formatted_value
                column_url = get_column_url(column)
                ending_values = ("А.В. Кузнецов", "В.В. Товаренко")

                if (not column_value) or (column_value in ending_values):
                    continue

                column_value = column_value.strip()

                if column_value.upper() in week_days:
                    last_week_day = column_value.upper()

                if column_value.replace(" ", "") in durations:
                    column_value = column_value.replace(" ", "")
                    column_value = {
                        "16.00-17-30": "16.00-17.30",
                        "17:00-18:30": "17.00-18.30",
                        "18:40-20:10": "18.40-20.10",
                    }.get(column_value, column_value)

                    last_duration = column_value

                if column_value.upper() in line_positions:
                    last_line_position = column_value.upper()

                    last_cords = ClassCords(
                        week_day=last_week_day,  # noqa
                        line_position=last_line_position,  # noqa
                        duration=last_duration,
                        row_index=int(row_index),
                    )

                # indexing groups
                if column_value.isdigit() and int(column_value) >= 100:
                    # index - index of column that contains related group classes
                    group_indexes[int(column_value)] = index
                    group_indexes[f"index;{index}"] = int(column_value)

                if index in group_indexes.values() and last_cords:
                    group_number = group_indexes[f"index;{index}"]
                    last_cords.group_number = int(group_number)

                    if column_url:
                        classes.append(
                            ScraperResult(
                                **last_cords.dict(),
                                value=column_value + f"\n\nСсылка: {column_url}",
                            )
                        )
                    else:
                        classes.append(
                            ScraperResult(
                                **last_cords.dict(),
                                value=column_value,
                            )
                        )

        final_classes += classes

    return final_classes


"""

nest classes inside groups

if column_value.isdigit():
    # index - index of column that contains related group classes
    group_indexes[int(column_value)] = index
    group_indexes[f'index;{index}'] = int(column_value)

    classes[int(column_value)] = {}

if index in group_indexes.values() and last_cords:
    group_number = group_indexes[f'index;{index}']

    saved_classes = classes[group_number].get(last_cords, [])
    saved_classes.append(column_value)
    classes[group_number][last_cords] = saved_classes
"""
