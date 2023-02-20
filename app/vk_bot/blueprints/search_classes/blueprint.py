import json
from datetime import datetime
from datetime import timedelta

from vkbottle.bot import Blueprint
from vkbottle.bot import Message

from app.backend.handlers.users.schemes import UserSchema
from app.vk_bot.blueprints.search_classes.services import compose_classes
from app.vk_bot.blueprints.search_classes.services import group_index_set
from app.vk_bot.blueprints.search_classes.triggers import TODAY_CLASSES_TRIGGERS
from app.vk_bot.blueprints.search_classes.triggers import TOMORROW_CLASSES_TRIGGERS
from app.vk_bot.keyboards.feedback import compose_feedback_keyboard
from app.vk_bot.rules.contains_trigger import ContainsTriggerRule

blueprint = Blueprint()


@blueprint.on.message(ContainsTriggerRule(TODAY_CLASSES_TRIGGERS, ["today"]))
async def today_classes_filter(message: Message, user: UserSchema):
    if not await group_index_set(message=message, user=user):
        return

    searching_date = datetime.now()

    final_message = await compose_classes(
        group_index=str(user.group_index),
        searching_date=searching_date,
    )

    keyboard = compose_feedback_keyboard({"grp": user.group_index, "srf": str(searching_date)})
    await message.answer(final_message, keyboard=keyboard)


@blueprint.on.message(ContainsTriggerRule(TOMORROW_CLASSES_TRIGGERS, ["tomorrow"]))
async def tomorrow_classes_filter(message: Message, user: UserSchema):
    if not await group_index_set(message=message, user=user):
        return

    searching_date = datetime.now() + timedelta(days=1)

    final_message = await compose_classes(
        group_index=str(user.group_index),
        searching_date=searching_date,
    )

    keyboard = compose_feedback_keyboard({"grp": user.group_index, "srf": str(searching_date)})
    await message.answer(final_message, keyboard=keyboard)


@blueprint.on.message(ContainsTriggerRule(payload_triggers=["by day"]))
async def find_by_week_day(message: Message, user: UserSchema):
    """Отправляет пары по указанному дню недели"""

    if not await group_index_set(message=message, user=user):
        return

    payload = json.loads(message.payload)
    next_week = payload.get("next")
    searching_week_day = payload.get("day")
    current_week_day = datetime.now().isocalendar().weekday

    if searching_week_day > current_week_day:
        delta = searching_week_day - current_week_day
    elif searching_week_day == current_week_day:
        delta = 0
    else:
        delta = current_week_day - searching_week_day

    searching_date = datetime.now() + timedelta(days=delta)

    if next_week:
        searching_date += timedelta(days=7)

    final_message = await compose_classes(
        group_index=str(user.group_index),
        searching_date=searching_date,
    )

    keyboard = compose_feedback_keyboard({"grp": user.group_index, "srf": str(searching_date)})
    await message.answer(final_message, keyboard=keyboard)
