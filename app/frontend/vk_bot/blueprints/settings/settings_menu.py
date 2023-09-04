from datetime import datetime

from vkbottle.bot import Blueprint
from vkbottle.bot import Message

from app.frontend.vk_bot.keyboards.menu.menu import menu_keyboard
from app.frontend.vk_bot.keyboards.settings.settings import settings_keyboard
from app.frontend.vk_bot.misc.constants import CHANGE_GROUP_TRIGGERS
from app.frontend.vk_bot.misc.constants import SETTINGS_TRIGGERS
from app.frontend.vk_bot.misc.contains_trigger_rule import ContainsTriggerRule
from app.frontend.vk_bot.states.settings import ChangingGroupStates
from config import settings

blueprint = Blueprint()


@blueprint.on.message(ContainsTriggerRule(SETTINGS_TRIGGERS, ["settings"]))
async def settings_menu(message: Message, user: UserSchema):
    text = (
        f"Твоя/ваша группа: {user.group_index} \n\n"
        "Список команд:\n"
        "vk.com/@mpsu_schedule-vse-komandy-bota\n\n"
        "F.A.Q:\n"
        "https://vk.com/topic-206763355_48153565\n\n"
        "Если чё-то не работает, пиши мне @baboomka"
    )

    await message.answer(message=text, keyboard=settings_keyboard)


@blueprint.on.message(ContainsTriggerRule(CHANGE_GROUP_TRIGGERS, ["change group"]))
async def group_picking_handler(message: Message):
    state = ChangingGroupStates.PICKING_GROUP

    await blueprint.state_dispenser.set(message.peer_id, state)
    await message.answer("Напиши номер своей группы")


@blueprint.on.message(state=ChangingGroupStates.PICKING_GROUP)
async def group_picking_handler(message: Message):
    is_digit = message.text.isdigit()

    if not is_digit:
        await message.answer(f"Напиши цифру, а не {message.text}")
        return

    group_number = int(message.text)

    if group_number in settings.NOT_EXISTING_GROUPS:
        await message.answer("Такой группы не существует")
        return

    if group_number < 99 or group_number > 600:
        text = "Врёшь... Таких групп не существует" "\n\nПринимаются цифры от 100 до 600"
        await message.answer(text)
        return

    async with async_session() as session:
        await UserCRUD(session).update_group(message.peer_id, group_number)

    await message.answer(f"Выбрана группа: {message.text}", keyboard=menu_keyboard)
    await blueprint.state_dispenser.delete(message.peer_id)


@blueprint.on.message(ContainsTriggerRule(["uptime"], ["uptime"]))
async def uptime(message: Message):
    date_str = await get_last_updated()
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
    classes_uptime = date_obj.strftime("%H:%M, %d.%m.%Y")
    text = f"Расписание последний раз обновлялось в {classes_uptime}"

    await message.answer(message=text, keyboard=settings_keyboard)


@blueprint.on.message(ContainsTriggerRule(payload_triggers=["toggle chatbot"]))
async def toggle_chatbot(message: Message):
    await message.answer(message="Виртуальный собеседник отдыхает", keyboard=settings_keyboard)
