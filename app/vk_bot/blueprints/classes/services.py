from datetime import datetime, timedelta

from app.backend.classes.crud import ClassesREDIS
from app.backend.classes.schemas import DaySchema
from app.backend.users.schemas import UserSchema
from app.utils import safe_get, is_week_above
from vkbottle.bot import Message

from app.vk_bot.blueprints.classes.keyboards import class_keyboard
from app.vk_bot.blueprints.general.keyboards import change_group_keyboard

redis = ClassesREDIS()


async def send_classes(message: Message, user: UserSchema, week_day_index: int, next_week: bool = False):
    searching_week = datetime.today().isocalendar().week + next_week
    if week_day_index > 6:
        week_day_index -= 6
        searching_week += 1

    above_line = is_week_above(searching_week)

    day = await redis.get(group_id=user.group_index, week_day_index=week_day_index, above_line=above_line)

    payload = {
        'group_id': user.group_index,
        'week_day_index': week_day_index,
        'above_line': above_line,
        'searching_week': searching_week,
        'next_week': next_week
    }

    if user.group_index is None:
        text = 'Пожалуйста, укажи группу. Напиши "поменять группу" или нажми на кнопку внизу'
        await message.answer(text, keyboard=change_group_keyboard)

    elif day is None:
        text = 'Я не нашёл пары на сегодня, прости((( \n\nМогу попробовать поиск старым способом'
        await message.answer(text, keyboard=class_keyboard(payload))

    else:
        text = compose_message(day, payload)
        await message.answer(text, keyboard=class_keyboard(payload))


def compose_message(day: DaySchema, payload: dict):
    week = payload.get('searching_week')
    week_day_index = payload.get("week_day_index")
    above_line = payload.get("above_line")
    next_week = payload.get("next_week")

    current_week = datetime.today().isocalendar().week
    date = datetime.today() + timedelta(days=next_week * 7)

    line_map = {
        True: 'Над чертой',
        False: 'Под чертой',
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
        f'{next_week_map.get(week > current_week)}, '
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


def get_class_text(day: DaySchema, index: int):
    possible_class = safe_get(day.classes, index)
    result = ''

    if possible_class is not None:
        result += possible_class.text
        # result += f'\n\nСсылки: {possible_class.hyperlinks}' if len(possible_class.hyperlinks) > 0 else ''
        # TODO доделать ссылки

    return result


async def get_uptime():
    return await redis.get_uptime()
