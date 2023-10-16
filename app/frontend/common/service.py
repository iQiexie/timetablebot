from datetime import datetime

from app.backend.api.services.dto.classes import LinePositionEnum
from app.backend.api.services.dto.classes import WEEK_DAYS_NUMBERED
from app.backend.api.services.dto.classes import WeekDaysEnum
from app.frontend.clients.backend import BackendApi
from app.frontend.common.dto.user import DayRequest


def get_week_line_position(week_index: int) -> LinePositionEnum:
    if week_index % 2 != 0:
        return LinePositionEnum.ABOVE

    return LinePositionEnum.BELOW


def compose_header(
    week_day: WeekDaysEnum,
    week_index: int,
    line_position: LinePositionEnum,
    date: datetime,
    group_number: int,
) -> str:
    current_week = datetime.now().today().isocalendar().week
    week_order = {
        current_week == week_index: "Эта неделя",
        current_week > week_index: "Следующая неделя",
        current_week < week_index: "Предыдущая неделя",
    }[True]

    return (
        "("
        f"{week_day.title()}, "
        f"{line_position.title()} чертой, "
        f"{week_order}, "
        f"Группа {group_number}, "
        f'{date.strftime("%d.%m.%Y")}'
        ")"
    )


async def compose_classes(
    group_number: int,
    user_id: int,
    searching_date: datetime,
    backend_client: BackendApi,
    pattern: str = None,
) -> str:
    week_day_index = searching_date.astimezone().isocalendar().weekday
    week_index = searching_date.astimezone().isocalendar().week  # порядковый номер искомой недели
    week_day = WEEK_DAYS_NUMBERED.get(week_day_index)  # искомый день енамом
    line_position = get_week_line_position(week_index=week_index)
    next_week = week_index > datetime.now().isocalendar().week

    data = DayRequest(
        group_number=group_number,
        week_day=week_day,
        line_position=line_position,
        next_week=next_week,
        user_id=user_id,
    )

    if pattern:
        data.pattern = pattern
        classes = await backend_client.get_classes_pattern(data=data)
    else:
        classes = await backend_client.get_classes(data=data)

    header = compose_header(
        week_day=week_day,
        week_index=week_index,
        line_position=line_position,
        date=searching_date,
        group_number=group_number,
    )

    result = f"{header}\n\n{classes}\n{header}"

    if pattern:
        result += f'\n\n\n⚠️ Внимание! Это результат поиска по запросу "{pattern}"'

    return result
