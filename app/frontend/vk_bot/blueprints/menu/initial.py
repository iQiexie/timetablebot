import traceback

from vkbottle.bot import Blueprint, Message

from app.backend.db.models.action import ButtonsEnum
from app.frontend.dto.user import User
from app.frontend.vk_bot.keyboards.menu.menu import menu_keyboard
from app.frontend.vk_bot.keyboards.settings.change_group import change_group_keyboard
from app.frontend.vk_bot.misc.constants import MENU_TRIGGERS
from app.frontend.vk_bot.misc.contains_trigger_rule import ContainsTriggerRule
from app.frontend.vk_bot.misc.request_clients import RequestClients
from config import settings

blueprint = Blueprint()


@blueprint.on.message(ContainsTriggerRule(triggers=MENU_TRIGGERS, payload_triggers=["main menu"]))
async def hello_handler(message: Message = None, user: User = None) -> None:
    new_user = user.group_number is None

    if new_user:
        answer_message = (
            'Привет! Для начала работы с ботом тебе нужно написать "Старт" или "Начать", '
            "а потом тебе нужно поменять свою группу через настройки."
            "\n\nСписок команд:"
            "\n vk.com/@mpsu_schedule-vse-komandy-bota"
        )
        await message.answer(answer_message, keyboard=change_group_keyboard)

    try:
        if await blueprint.state_dispenser.get(message.peer_id):
            await blueprint.state_dispenser.delete(message.peer_id)
    except KeyError:
        traceback.print_exc()

    await message.answer(message=settings.VK_EMPTY_MESSAGE, keyboard=menu_keyboard)
    await RequestClients.backend.mark_action(user_id=user.id, button_name=ButtonsEnum.menu)
