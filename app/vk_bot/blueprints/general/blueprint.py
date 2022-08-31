from vkbottle.bot import Blueprint, Message

from app.backend.users.schemas import UserSchema
from app.vk_bot.blueprints.general.keyboards import change_group_keyboard, menu_keyboard, remove_keyboard
from app.vk_bot.blueprints.general.rules import MenuRule, KillKeyboardRule
from app.vk_bot.defaults import DEFAULT_ANSWER_MESSAGE

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
    await message.answer(DEFAULT_ANSWER_MESSAGE, keyboard=menu_keyboard())


@general_bp.on.message(KillKeyboardRule())
async def hello_handler(message: Message):
    text = (
        'Чтобы вернуть клавиатуру, напиши боту "Старт", "Начать" или "Привет"\n\n'
        'В случае с группами, напишите боту "Бот старт", "Бот начать" или "Бот привет"'
    )
    await message.answer(message=text, keyboard=remove_keyboard)
