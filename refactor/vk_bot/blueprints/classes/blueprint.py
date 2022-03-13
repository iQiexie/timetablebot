from datetime import datetime

from vkbottle.bot import Blueprint, Message

from refactor.backend.base.db import async_session
from refactor.backend.classes.crud import ClassesREDIS
from refactor.backend.users.crud import UserCRUD
from refactor.vk_bot.blueprints.general.rules import TodayClassesRule

classes_bp = Blueprint()


@classes_bp.on.message(TodayClassesRule())
async def today_classes_filter(message: Message):
    db = UserCRUD(async_session)
    classes = ClassesREDIS()

    user = await db.get(vk_id=message.peer_id)

    group_id = user.group_index
    week_day_index = datetime.today().isocalendar().weekday - 1
    above_line = datetime.today().isocalendar().week % 2 == 0

    classes = await classes.get(
        group_id=group_id,
        week_day_index=week_day_index,
        above_line=above_line,
    )

    if group_id is None:
        text = 'Пожалуйста, укажи группу. Напиши "поменять группу" или нажми на кнопку внизу'
        await message.answer(text)
        # TODO return keyboard with appropriate buttons
        return

    elif classes is None:
        text = 'Я не нашёл пары на сегодня, прости(((\n\nМогу попробовать поиск старым способом'
        await message.answer(text)
        # TODO return keyboard with appropriate buttons
        return

    else:
        await message.answer(classes)


@classes_bp.on.message(TodayClassesRule())
async def today_classes_filter(message: Message):
    db = UserCRUD(async_session)
    classes = ClassesREDIS()

    user = await db.get(vk_id=message.peer_id)

    group_id = user.group_index
    week_day_index = datetime.today().isocalendar().weekday
    above_line = datetime.today().isocalendar().week % 2 == 0

    if week_day_index > 6:
        week_day_index -= 6

    classes = await classes.get(
        group_id=group_id,
        week_day_index=week_day_index,
        above_line=above_line,
    )

    if group_id is None:
        text = 'Пожалуйста, укажи группу. Напиши "поменять группу" или нажми на кнопку внизу'
        await message.answer(text)
        # TODO return keyboard with appropriate buttons
        return

    elif classes is None:
        text = 'Я не нашёл пары на сегодня, прости(((\n\nМогу попробовать поиск старым способом'
        await message.answer(text)
        # TODO return keyboard with appropriate buttons
        return

    else:
        await message.answer(classes)
