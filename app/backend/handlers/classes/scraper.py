from app.backend.handlers.classes.schemes import DURATIONS_MAP
from app.backend.handlers.classes.schemes import SheetValue
from app.backend.libs.google_scheets.main import GoogleAPI
from app.backend.redis.utils import compose_key


def get_column_url(column: SheetValue) -> str:
    for format_runs in column.text_format_runs or []:
        if not format_runs.format.link:
            continue

        if url := format_runs.format.link.uri:
            return url


async def scrape_spreadsheet() -> dict:
    google = GoogleAPI()
    await google.init_services()

    final_classes = []

    for grade in range(1, 6):
        print(f"Parsing grade: {grade}")
        sheet = await google.read_sheet(grade)

        group_indexes = {}
        week_days = ("ПОНЕДЕЛЬНИК", "ВТОРНИК", "СРЕДА", "ЧЕТВЕРГ", "ПЯТНИЦА", "СУББОТА")
        durations = DURATIONS_MAP.keys()
        line_positions = ("НАД", "ПОД")

        classes = {}
        last_week_day = None
        last_duration = None
        last_cords = None

        for row_index, row in enumerate(sheet.rowData):
            if not row.values:
                continue

            for index, column in enumerate(row.values):
                column_value = column.formatted_value.strip() if column.formatted_value else None
                column_url = get_column_url(column)

                ending_values = ("А.В. Кузнецов", "В.В. Товаренко")

                if not column_value or column_value in ending_values:
                    continue

                if column_value.upper() in week_days:
                    last_week_day = column_value.upper()

                if column_value in durations:
                    if column_value == "16.00-17-30":
                        column_value = "16.00-17.30"
                    last_duration = column_value

                if column_value.upper() in line_positions:
                    last_line_position = column_value.upper()
                    last_cords = compose_key(
                        last_week_day,
                        last_line_position,
                        last_duration,
                        str(row_index),
                    )

                # indexing groups
                if column_value.isdigit():
                    # index - index of column that contains related group classes
                    group_indexes[int(column_value)] = index
                    group_indexes[f"index;{index}"] = int(column_value)

                if index in group_indexes.values() and last_cords:
                    group_number = group_indexes[f"index;{index}"]
                    full_cords = compose_key(str(group_number), last_cords)
                    if column_url:
                        classes[full_cords] = column_value + f"\n\nСсылка: {column_url}"
                    else:
                        classes[full_cords] = column_value

        final_classes.append(classes)

    result = {}
    for classes in final_classes:
        result.update(classes)

    return result


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
