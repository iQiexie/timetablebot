from vkbottle.bot import Blueprint
from vkbottle.bot import Message

from app.vk_bot.keyboards.remove import remove_keyboard
from app.vk_bot.rules.contains_trigger import ContainsTriggerRule

blueprint = Blueprint()


@blueprint.on.message(ContainsTriggerRule(payload_triggers=['suicide']))
async def kill_keyboard(message: Message):
    text = (
        'Чтобы вернуть клавиатуру, напиши боту "Старт", "Начать" или "Привет"\n\n'
        'Если я живу в беседе группы, добавь к каждой команде слово "Бот": "Бот старт" и т.д'
    )
    await message.answer(message=text, keyboard=remove_keyboard)
