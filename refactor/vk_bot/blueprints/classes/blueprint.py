import json
from datetime import datetime
from vkbottle.bot import Blueprint, Message

from refactor.backend.users.schemas import UserSchema
from refactor.vk_bot.blueprints.classes.legacy.ClassProcessor import ClassProcessor
from refactor.vk_bot.blueprints.classes.services import send_classes
from refactor.vk_bot.blueprints.classes.rules import (
    TodayClassesRule,
    TomorrowClassesRule,
    LegacySearchRule,
    DownVoteRule
)

classes_bp = Blueprint()


@classes_bp.on.message(TodayClassesRule())
async def today_classes_filter(message: Message, user: UserSchema):
    week_day_index = datetime.today().isocalendar().weekday - 1

    await send_classes(message, user, week_day_index)


@classes_bp.on.message(TomorrowClassesRule())
async def tomorrow_classes_filter(message: Message, user: UserSchema):
    week_day_index = datetime.today().isocalendar().weekday

    await send_classes(message, user, week_day_index)


@classes_bp.on.message(DownVoteRule())
async def tomorrow_classes_filter(message: Message, user: UserSchema):
    await message.answer('Ну всё пиздец теперь. #TODO доделать')  # TODO доделать


@classes_bp.on.message(LegacySearchRule())
async def legacy_search(message: Message, user: UserSchema):
    cp = ClassProcessor()
    await cp.init(user.group_index)

    payload = json.loads(message.payload)

    searching_week = datetime.today().isocalendar().week
    next_week = searching_week > payload.get('week')

    text = cp.getByDay(week_day_index=payload.get('week_day_index'), next_week=next_week)

    await message.answer(text)
