from datetime import datetime, timedelta

from vkbottle.bot import Blueprint, Message

from refactor.backend.classes.crud import ClassesREDIS
from refactor.backend.classes.schemas import DaySchema
from refactor.backend.users.schemas import UserSchema
from refactor.utils import safe_get
from refactor.vk_bot.blueprints.classes.keyboards import get_legacy_search_keyboard
from refactor.vk_bot.blueprints.classes.rules import TodayClassesRule, TomorrowClassesRule, LegacySearchRule
from refactor.vk_bot.blueprints.general.keyboards import change_group_keyboard

classes_bp = Blueprint()
classes = ClassesREDIS()


@classes_bp.on.message(TodayClassesRule())
async def today_classes_filter(message: Message, user: UserSchema):
    week_day_index = datetime.today().isocalendar().weekday - 1

    await send_classes(message, user, week_day_index)


@classes_bp.on.message(TomorrowClassesRule())
async def tomorrow_classes_filter(message: Message, user: UserSchema):
    week_day_index = datetime.today().isocalendar().weekday

    await send_classes(message, user, week_day_index)


@classes_bp.on.message(LegacySearchRule())
async def tomorrow_classes_filter(message: Message):
    await message.answer(f'legacy search { message.payload=}')


def get_class_text(day: DaySchema, index: int):
    possible_class = safe_get(day.classes, index)
    if possible_class is not None:
        return possible_class.text
    else:
        return ""


async def send_classes(message: Message, user: UserSchema, week_day_index: int):
    group_id = user.group_index
    above_line = datetime.today().isocalendar().week % 2 == 0
    searching_week = datetime.today().isocalendar().week

    if week_day_index > 6:
        week_day_index -= 6
        searching_week += 1

    day = await classes.get(group_id=group_id, week_day_index=week_day_index, above_line=above_line)

    payload = {
        'group_id': group_id,
        'week_day_index': week_day_index,
        'above_line': above_line,
        'week': searching_week,
    }

    if group_id is None:
        text = 'Пожалуйста, укажи группу. Напиши "поменять группу" или нажми на кнопку внизу'
        await message.answer(text, keyboard=change_group_keyboard)

    elif day is None:
        text = 'Я не нашёл пары на сегодня, прости((( \n\nМогу попробовать поиск старым способом'
        await message.answer(text, keyboard=get_legacy_search_keyboard(payload))

    else:
        text = compose_message(day, payload)
        await message.answer(text)


def compose_message(day: DaySchema, payload: dict):
    week = payload.get('week')
    week_day_index = payload.get("week_day_index")
    above_line = payload.get("above_line")

    current_week = datetime.today().isocalendar().week
    date = datetime.today() + timedelta(days=above_line * 7)

    line_map = {
        False: 'Над чертой',
        True: 'Под чертой',
    }

    next_week_map = {
        False: 'Эта неделя',
        True: 'Следующая неделя',
    }

    week_day_map = {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница',
        5: 'Суббота',
        6: 'Воскресенье',
    }

    footer_header = (
        '('
        f'{week_day_map.get(week_day_index)}, '
        f'{line_map.get(above_line)}, '
        f'{next_week_map.get(week == current_week)}, '
        f'{date.strftime("%d.%m.%Y")}'
        ')'
    )

    message = (
        f'\n{footer_header}\n'
        '\n[09:00 - 10:30]:\n'
        f'\n{get_class_text(day, 0)}\n'
        '\n[10:40 - 12:10]:\n'
        f'\n{get_class_text(day, 1)}\n'
        '\n[12:40 - 14:10]::\n'
        f'\n{get_class_text(day, 2)}\n'
        '\n[14:20 - 15:50]:\n'
        f'\n{get_class_text(day, 3)}\n'
        '\n[16:00 - 17:30]:\n'
        f'\n{get_class_text(day, 4)}\n'
        f'\n{footer_header}\n'
    )

    return message
