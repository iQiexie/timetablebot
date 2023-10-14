from vkbottle.bot import Blueprint
from vkbottle.bot import Message

from app.backend.db.models.action import ButtonsEnum
from app.frontend.dto.enum import SourcesEnum
from app.frontend.dto.user import User
from app.frontend.vk_bot.keyboards.menu.remove import remove_keyboard
from app.frontend.vk_bot.misc.contains_trigger_rule import ContainsTriggerRule
from app.frontend.vk_bot.misc.request_clients import RequestClients

blueprint = Blueprint()


@blueprint.on.message(ContainsTriggerRule(payload_triggers=["suicide"]))
async def kill_keyboard(message: Message, user: User) -> None:
    text = (
        'Чтобы вернуть клавиатуру, напиши боту "Старт" или "Начать"\n\n'
        'Если я живу в беседе группы, добавь к каждой команде слово "Бот": "Бот старт" и т.д'
    )
    await message.answer(message=text, keyboard=remove_keyboard)
    await RequestClients.backend.mark_action(
        source=SourcesEnum.vk,
        user_id=user.id,
        button_name=ButtonsEnum.kill_keyboard,
    )
