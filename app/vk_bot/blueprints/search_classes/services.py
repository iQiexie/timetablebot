from datetime import datetime

from vkbottle.bot import Message

from app.backend.handlers.classes.enums import LinePositionEnum
from app.backend.handlers.classes.enums import WEEK_DAYS_NUMBERED
from app.backend.handlers.classes.enums import WeekDaysEnum
from app.backend.handlers.classes.handler import find_day
from app.backend.handlers.classes.handler import get_week_line_position
from app.backend.handlers.users.schemes import UserSchema
from app.vk_bot.keyboards.change_group import change_group_keyboard


async def group_index_set(message: Message, user: UserSchema) -> bool:
    if not user.group_index:
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
    group_index: str,
    searching_date: datetime,
    pattern: str = None,
):
    week_day_index = searching_date.isocalendar().weekday  # пор. номер искомого дня недели
    week_index = searching_date.isocalendar().week  # порядковый номер искомой недели
    week_day = WEEK_DAYS_NUMBERED.get(week_day_index)  # искомый день енамом
    line_position = get_week_line_position(week_index=week_index)

    classes = await find_day(
        group_number=group_index,
        week_day=week_day,
        line_position=line_position,
        pattern=pattern,
    )

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
