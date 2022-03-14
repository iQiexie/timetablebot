import json
from datetime import datetime
from vkbottle.bot import Blueprint, Message

from config import settings
from app.backend.users.schemas import UserSchema
from app.vk_bot.blueprints.classes.keyboards import by_day_keyboard
from app.vk_bot.blueprints.classes.legacy.ClassProcessor import ClassProcessor
from app.vk_bot.blueprints.classes.services import send_classes
from app.vk_bot.blueprints.classes.rules import (
    TodayClassesRule,
    TomorrowClassesRule,
    LegacySearchRule,
    DownVoteRule,
    UpVoteRule,
    DaySelectionRule,
    ByDayRule
)
from app.vk_bot.defaults import DEFAULT_ANSWER_MESSAGE

classes_bp = Blueprint()


@classes_bp.on.message(TodayClassesRule())
async def today_classes_filter(message: Message, user: UserSchema):
    """ Отправляет пары на сегодня """

    week_day_index = datetime.today().isocalendar().weekday - 1

    await send_classes(message, user, week_day_index)


@classes_bp.on.message(TomorrowClassesRule())
async def tomorrow_classes_filter(message: Message, user: UserSchema):
    """ Отправляет пары на завтра """

    week_day_index = datetime.today().isocalendar().weekday

    await send_classes(message, user, week_day_index)


@classes_bp.on.message(ByDayRule())
async def find_by_day(message: Message, user: UserSchema):
    """ Отправляет пары по указанному дню недели """

    payload = json.loads(message.payload)
    week_day_index = payload.get('day')
    next_week = payload.get('next')

    await send_classes(message, user, week_day_index, next_week)


@classes_bp.on.message(DaySelectionRule())
async def day_selection(message: Message):
    """ Отправляет клавиатуру с выбором дня """

    payload = json.loads(message.payload)
    next_week = payload.get('next')
    await message.answer(keyboard=by_day_keyboard(next_week), message=DEFAULT_ANSWER_MESSAGE)


@classes_bp.on.message(DownVoteRule())
async def downvote(message: Message, user):
    """ Отправляет админу о некорректной паре """

    text = (
        f'Пользователю: {user.vk_id}\n\n'
        f'Пришли невалидные пары:\n\n'
        f'{message.payload}'
    )
    await message.ctx_api.messages.send(peer_ids=settings.ADMIN_VK_IDS, random_id=0, message=text)
    await message.answer("Обратная связь учтена. Спасибо 💖")


@classes_bp.on.message(UpVoteRule())
async def upvote(message: Message):
    """ Ничего не делает, просто высылает фидбек юзверу """

    await message.answer("Обратная связь учтена. Спасибо 💖")


@classes_bp.on.message(LegacySearchRule())
async def legacy_search(message: Message, user: UserSchema):
    """ Ищет пары по тому же самому дню старым способом """

    cp = ClassProcessor()
    await cp.init(user.group_index)

    payload = json.loads(message.payload)

    searching_week = datetime.today().isocalendar().week
    next_week = searching_week > payload.get('searching_week')

    text = cp.getByDay(week_day_index=payload.get('week_day_index'), next_week=next_week)

    await message.answer(text)
