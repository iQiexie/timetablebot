from datetime import datetime

from vkbottle.bot import Message

from app.backend.api.services.dto.classes import LinePositionEnum
from app.backend.api.services.dto.classes import WEEK_DAYS_NUMBERED
from app.backend.api.services.dto.classes import WeekDaysEnum
from app.frontend.dto.user import DayRequest
from app.frontend.dto.user import User
from app.frontend.vk_bot.keyboards.settings.change_group import change_group_keyboard
from app.frontend.vk_bot.misc.request_clients import RequestClients


def get_week_line_position(week_index: int) -> LinePositionEnum:
    if week_index % 2 != 0:
        return LinePositionEnum.ABOVE

    return LinePositionEnum.BELOW


async def group_index_set(message: Message, user: User) -> bool:
    if not user.group_number:
        text = 'Пожалуйста, укажи группу. Напиши "поменять группу" или нажми на кнопку внизу'
        await message.answer(text, keyboard=change_group_keyboard)
        return False

    return True


def compose_header(
    week_day: WeekDaysEnum,
    week_index: int,
    line_position: LinePositionEnum,
    date: datetime,
) -> str:
    current_week = datetime.now().today().isocalendar().week
    week_order = "Эта неделя" if current_week == week_index else "Следующая неделя"

    return (
        "("
        f"{week_day.title()}, "
        f"{line_position.title()} чертой, "
        f"{week_order}, "
        f'{date.strftime("%d.%m.%Y")}'
        ")"
    )


async def compose_classes(
    group_number: int,
    vk_id: int,
    searching_date: datetime,
    pattern: str = None,
) -> None:
    week_day_index = searching_date.isocalendar().weekday  # пор. номер искомого дня недели
    week_index = searching_date.isocalendar().week  # порядковый номер искомой недели
    week_day = WEEK_DAYS_NUMBERED.get(week_day_index)  # искомый день енамом
    line_position = get_week_line_position(week_index=week_index)
    next_week = week_index > datetime.now().isocalendar().week

    data = DayRequest(
        group_number=group_number,
        week_day=week_day,
        line_position=line_position,
        next_week=next_week,
        vk_id=vk_id,
    )

    if pattern:
        data.pattern = pattern
        classes = await RequestClients.backend.get_classes_pattern(data=data)
    else:
        classes = await RequestClients.backend.get_classes(data=data)

    header = compose_header(
        week_day=week_day,
        week_index=week_index,
        line_position=line_position,
        date=searching_date,
    )

    result = f"{header}\n\n{classes}\n{header}"

    if pattern:
        result += f'\n\n\nВнимание! Это результат поиска по запросу "{pattern}"'

    return result
