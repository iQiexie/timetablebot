import json
from datetime import datetime
from datetime import timedelta

from vkbottle.bot import Blueprint
from vkbottle.bot import Message

from app.frontend.dto.user import User
from app.frontend.vk_bot.keyboards.classes.feedback import compose_feedback_keyboard
from app.frontend.vk_bot.keyboards.classes.week import compose_detailed_menu
from app.frontend.vk_bot.keyboards.classes.week import compose_week_keyboard
from app.frontend.vk_bot.keyboards.classes.week import reset_keyboard
from app.frontend.vk_bot.misc.classes_service import compose_classes
from app.frontend.vk_bot.misc.classes_service import group_index_set
from app.frontend.vk_bot.misc.constants import TODAY_CLASSES_TRIGGERS
from app.frontend.vk_bot.misc.constants import TOMORROW_CLASSES_TRIGGERS
from app.frontend.vk_bot.misc.contains_trigger_rule import ContainsTriggerRule
from app.frontend.vk_bot.states.classes import ClassStates
from config import settings

blueprint = Blueprint()


@blueprint.on.message(ContainsTriggerRule(TODAY_CLASSES_TRIGGERS, ["today"]))
async def today_classes_filter(message: Message, user: User):
    if not await group_index_set(message=message, user=user):
        return

    searching_date = datetime.now()

    final_message = await compose_classes(
        group_number=user.group_number,
        searching_date=searching_date,
        vk_id=message.peer_id,
    )

    keyboard = compose_feedback_keyboard({"grp": user.group_number, "srf": str(searching_date)})
    await message.answer(final_message, keyboard=keyboard)


@blueprint.on.message(ContainsTriggerRule(TOMORROW_CLASSES_TRIGGERS, ["tomorrow"]))
async def tomorrow_classes_filter(message: Message, user: User):
    if not await group_index_set(message=message, user=user):
        return

    searching_date = datetime.now() + timedelta(days=1)

    final_message = await compose_classes(
        group_number=user.group_number,
        searching_date=searching_date,
        vk_id=message.peer_id,
    )

    keyboard = compose_feedback_keyboard({"grp": user.group_number, "srf": str(searching_date)})
    await message.answer(final_message, keyboard=keyboard)


@blueprint.on.message(ContainsTriggerRule(payload_triggers=["by day"]))
async def find_by_week_day(message: Message, user: User):
    """Отправляет пары по указанному дню недели"""

    payload = json.loads(message.payload)
    next_week = payload.get("next")
    searching_week_day = payload.get("day")
    pattern = payload.get("match")
    current_week_day = datetime.now().isocalendar().weekday

    if not pattern and not await group_index_set(message=message, user=user):
        return

    if searching_week_day == current_week_day:
        delta = 0
    else:
        delta = searching_week_day - current_week_day

    searching_date = datetime.now() + timedelta(days=delta)

    if next_week:
        searching_date += timedelta(days=7)

    final_message = await compose_classes(
        group_number=user.group_number,
        searching_date=searching_date,
        pattern=pattern,
        vk_id=message.peer_id,
    )

    keyboard = compose_feedback_keyboard({"grp": user.group_number, "srf": str(searching_date)})
    await message.answer(final_message, keyboard=keyboard)


@blueprint.on.message(ContainsTriggerRule(payload_triggers=["pattern_search"]))
async def pattern_search(message: Message):
    greeting = (
        "Добро пожаловать в поиск по шаблону. В этом разделе можно найти все пары, "
        "в названии которых содержится твой запрос (шаблон) \n\n"
        "Например, если ты напишешь имя (или часть имени) преподавателя, то бот отправит тебе его "
        "расписание"
    )

    await message.answer(greeting)
    await message.answer("Напиши мне свой запрос, а потом выбери нужный день")
    await blueprint.state_dispenser.set(message.peer_id, ClassStates.WAITING_FOR_PATTERN)


@blueprint.on.message(state=ClassStates.WAITING_FOR_PATTERN)
async def search_by_pattern(message: Message):
    keyboard = compose_detailed_menu(pattern=message.text)
    await message.answer("Готово, теперь выбери нужную неделю и день", keyboard=keyboard)
    await blueprint.state_dispenser.delete(message.peer_id)


@blueprint.on.message(ContainsTriggerRule(payload_triggers=["sweek"]))
async def day_selection(message: Message):
    """Отправляет клавиатуру с выбором дня"""

    payload = json.loads(message.payload)
    next_week = payload.get("next")
    match = payload.get("match")

    if match:
        keyboard = compose_week_keyboard(next_week=next_week, pattern=match)
    else:
        keyboard = compose_week_keyboard(next_week=next_week)

    await message.answer(message=settings.VK_EMPTY_MESSAGE, keyboard=keyboard)


@blueprint.on.message(ContainsTriggerRule(payload_triggers=["detailed"]))
async def detailed_search(message: Message):
    """Отправляет клавиатуру с выбором недели и паттерн поиском"""
    payload = json.loads(message.payload)
    pattern = payload.get("match")

    if pattern:
        keyboard = compose_detailed_menu(pattern=pattern)
    else:
        keyboard = compose_detailed_menu()

    await message.answer(message=settings.VK_EMPTY_MESSAGE, keyboard=keyboard)


@blueprint.on.message(ContainsTriggerRule(payload_triggers=["searching_status"]))
async def searching_status(message: Message):
    text = (
        f"Эта кнопка ничего не делает. Она лишь показывает, в каком статусе сейчас "
        f"находится бот."
    )

    await message.answer(text, keyboard=reset_keyboard)
