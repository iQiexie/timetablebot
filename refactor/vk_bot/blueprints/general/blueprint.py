from vkbottle.bot import Blueprint, Message

from app.Assets.Strings import DEFAULT_ANSWER_MESSAGE
from refactor.backend.users.schemas import UserSchema
from refactor.vk_bot.blueprints.general.keyboards import change_group_keyboard, menu_keyboard
from refactor.vk_bot.blueprints.general.rules import MenuRule

general_bp = Blueprint()


@general_bp.on.message(MenuRule())
async def hello_handler(message: Message, user: UserSchema):
    new_user = user.group_index is None

    if new_user:
        answer_message = (
            'Привет! Для начала работы с ботом тебе нужно написать "Старт" или "Начать", '
            'а потом тебе нужно поменять свою группу через настройки.'
            '\n\nСписок команд:'
            '\n vk.com/@mpsu_schedule-vse-komandy-bota'
        )
        await message.answer(answer_message, keyboard=change_group_keyboard)
    await message.answer(DEFAULT_ANSWER_MESSAGE, keyboard=menu_keyboard)
