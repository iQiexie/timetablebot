import json

from vkbottle.bot import Blueprint
from vkbottle.bot import Message

from app.vk_bot.keyboards.week_current import current_week_keyboard
from app.vk_bot.keyboards.week_next import next_week_keyboard
from app.vk_bot.rules.contains_trigger import ContainsTriggerRule
from config import settings

blueprint = Blueprint()


@blueprint.on.message(ContainsTriggerRule(payload_triggers=["sweek"]))
async def day_selection(message: Message):
    """Отправляет клавиатуру с выбором дня"""

    payload = json.loads(message.payload)
    next_week = payload.get("next")

    if next_week:
        keyboard = next_week_keyboard
    else:
        keyboard = current_week_keyboard

    await message.answer(message=settings.VK_EMPTY_MESSAGE, keyboard=keyboard)
