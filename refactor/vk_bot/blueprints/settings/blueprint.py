from vkbottle.bot import Blueprint, Message

from app.Assets.Strings import DEFAULT_ANSWER_MESSAGE
from refactor.backend.base.db import async_session
from refactor.backend.users.crud import UserCRUD
from refactor.backend.users.schemas import UserSchema
from refactor.vk_bot.blueprints.classes.services import get_uptime
from refactor.vk_bot.blueprints.general.keyboards import menu_keyboard
from refactor.vk_bot.blueprints.settings.rules import SettingsRule, ChangeGroupRule, UptimeRule, ChatBotSettingsRule
from refactor.vk_bot.blueprints.settings.keyboards import settings_keyboard
from refactor.vk_bot.misc.states import PickingState

settings_bp = Blueprint()
db = UserCRUD(async_session)


@settings_bp.on.message(SettingsRule())
async def send_settings_keyboard_handler(message: Message, user: UserSchema):
    text = (
                f"Твоя/ваша группа: {user.group_index} \n\n"
                "Список команд:\n"
                "vk.com/@mpsu_schedule-vse-komandy-bota\n\n"
                "F.A.Q:\n"
                "https://vk.com/topic-206763355_48153565\n\n"
                "Если чё-то не работает, пиши мне @baboomka"
    )

    await message.answer(keyboard=settings_keyboard, message=text)


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

        await message.answer(f"Группа выбрана. Она: {message.text}", keyboard=menu_keyboard())
        await settings_bp.state_dispenser.delete(message.peer_id)
        await db.update(message.peer_id, group_index=int(message.text))
    else:
        await message.answer(f"Напиши цифру, а не {message.text}")


@settings_bp.on.message(UptimeRule())
async def tomorrow_classes_filter(message: Message):
    uptime = await get_uptime()
    text = f'Расписание последний раз обновлялось в {uptime}'
    await message.answer(text)


@settings_bp.on.message(ChatBotSettingsRule())
async def tomorrow_classes_filter(message: Message):
    await message.answer(f"Виртуальный собеседник отдыхает")


