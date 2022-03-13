from vkbottle.bot import Blueprint, Message

from app.Assets.Strings import DEFAULT_ANSWER_MESSAGE
from refactor.vk_bot.blueprints.settings.rules import GeneralRule, ChangeGroupRule
from refactor.vk_bot.blueprints.settings.keyboards import settings_keyboard
from refactor.vk_bot.misc.states import PickingState

settings_bp = Blueprint()


@settings_bp.on.message(GeneralRule())
async def send_settings_keyboard_handler(message: Message):
    await message.answer(keyboard=settings_keyboard, message=DEFAULT_ANSWER_MESSAGE)


@settings_bp.on.message(ChangeGroupRule())
async def group_picking_handler(message: Message):
    state = PickingState.PICKING_GROUP
    error_message = 'Принимаются ответы только в цифрах от 100 до 500'

    await settings_bp.state_dispenser.set(message.peer_id, state, error=error_message)
    await message.answer('Напиши номер своей группы')


@settings_bp.on.message(state=PickingState.PICKING_GROUP)
async def group_picking_handler(message: Message):
    is_digit = message.text.isdigit()

    if is_digit:
        if int(message.text) < 99 or int(message.text) > 420:
            await message.answer("Врёшь, не проведёшь... Таких групп не существует")
            return

        await message.answer(f"Группа выбрана. Она: {message.text}")
        await settings_bp.state_dispenser.delete(message.peer_id)
    else:
        await message.answer(f"Напиши цифру, а не {message.text}")



