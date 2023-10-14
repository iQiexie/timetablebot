import urllib.parse
from datetime import datetime
from datetime import timedelta

from aiogram import F
from aiogram import Router
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from app.backend.db.models.action import ButtonsEnum
from app.frontend.clients.telegram import TelegramClient
from app.frontend.dto.enum import SourcesEnum
from app.frontend.dto.user import User
from app.frontend.singletons import Clients
from app.frontend.tg_bot.keyboards.classes import get_week_keyboard
from app.frontend.tg_bot.keyboards.feedback import get_feedback_keyboard
from app.frontend.tg_bot.keyboards.menu import get_detailed_menu
from app.frontend.tg_bot.misc.callbacks import Callback
from app.frontend.tg_bot.misc.callbacks import CallbackActions
from app.frontend.tg_bot.misc.states import FSMStates
from app.frontend.tg_bot.services.classes import group_index_set
from app.frontend.vk_bot.misc.classes_service import compose_classes
from app.frontend.vk_bot.misc.request_clients import RequestClients
from config import settings

class_search_router = Router()


@class_search_router.callback_query(Callback.filter(F.action.in_({CallbackActions.today})))
async def today_classes_filter(query: CallbackQuery, current_user: User) -> None:
    if not await group_index_set(message=query, user=current_user):
        return

    searching_date = datetime.now()
    keyboard = get_feedback_keyboard(
        searching_date=searching_date.timestamp(),
        back=CallbackActions.menu,
    )
    final_message = await compose_classes(
        group_number=current_user.group_number,
        searching_date=searching_date,
        user_id=current_user.id,
    )

    await query.answer(settings.TELEGRAM_EMPTY_MESSAGE)
    await TelegramClient.send_message(
        query=query,
        text=final_message,
        reply_markup=keyboard,
    )


@class_search_router.callback_query(Callback.filter(F.action.in_({CallbackActions.tomorrow})))
async def tomorrow_classes_filter(query: CallbackQuery, current_user: User) -> None:
    if not await group_index_set(message=query, user=current_user):
        return

    searching_date = datetime.now() + timedelta(days=1)
    keyboard = get_feedback_keyboard(
        searching_date=searching_date.timestamp(),
        back=CallbackActions.menu,
    )
    final_message = await compose_classes(
        group_number=current_user.group_number,
        searching_date=searching_date,
        user_id=current_user.id,
    )

    await query.answer(settings.TELEGRAM_EMPTY_MESSAGE)
    await TelegramClient.send_message(
        query=query,
        text=final_message,
        reply_markup=keyboard,
    )


@class_search_router.callback_query(Callback.filter(F.action.in_({CallbackActions.by_day})))
async def find_by_week_day(
    query: CallbackQuery,
    callback_data: Callback,
    current_user: User,
    state: FSMContext,
) -> None:
    """Отправляет пары по указанному дню недели"""
    await query.answer(settings.TELEGRAM_EMPTY_MESSAGE)
    state_data = await state.get_data()

    payload = urllib.parse.parse_qs(callback_data.data)
    searching_week_day = int(payload["d"][0])
    next_week = "next" in payload["w"][0]
    pattern = state_data.get("pattern")
    current_week_day = datetime.now().isocalendar().weekday

    if not pattern and not await group_index_set(message=query, user=current_user):
        return

    if searching_week_day == current_week_day:
        delta = 0
    else:
        delta = searching_week_day - current_week_day

    searching_date = datetime.now() + timedelta(days=delta)

    if next_week:
        searching_date += timedelta(days=7)

    final_message = await compose_classes(
        group_number=current_user.group_number,
        searching_date=searching_date,
        pattern=pattern,
        user_id=current_user.id,
    )

    keyboard = get_feedback_keyboard(
        searching_date=searching_date.timestamp(),
        back=CallbackActions.sweak,
        back_payload={"w": payload["w"][0]},
    )

    await TelegramClient.send_message(
        query=query,
        text=final_message,
        reply_markup=keyboard,
    )


@class_search_router.message(state=FSMStates.pattern_input)
async def search_by_pattern(message: Message, state: FSMContext) -> None:
    keyboard = get_detailed_menu(pattern=message.text)

    await Clients.telegram.send_message(
        query=message,
        text="Готово, теперь выбери нужную неделю и день",
        reply_markup=keyboard,
    )

    await state.set_state(state=FSMStates.pattern_search)
    await state.set_data(data={"pattern": message.text})


@class_search_router.callback_query(Callback.filter(F.action.in_({CallbackActions.sweak})))
async def day_selection(query: CallbackQuery, callback_data: Callback, current_user: User) -> None:
    """Отправляет клавиатуру с выбором дня"""

    next_week = "next" in callback_data.data
    match = callback_data.data.split(",")[-1] or ""
    header = "Выбрана неделя: следующая" if next_week else "Выбрана неделя: текущая"
    keyboard = get_week_keyboard(next_week=next_week)

    await query.answer(settings.TELEGRAM_EMPTY_MESSAGE)
    await TelegramClient.send_message(
        query=query,
        text=header,
        reply_markup=keyboard,
    )

    button_name = {
        next_week is True and match is not None: ButtonsEnum.next_week_pattern,
        next_week is False and match is not None: ButtonsEnum.current_week_pattern,
        next_week is True and match is None: ButtonsEnum.next_week,
        next_week is False and match is None: ButtonsEnum.current_week,
    }.get(True)

    await RequestClients.backend.mark_action(
        source=SourcesEnum.telegram,
        user_id=current_user.id,
        button_name=button_name,
        pattern=match,
    )
