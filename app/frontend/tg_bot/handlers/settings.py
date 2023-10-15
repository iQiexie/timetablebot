from aiogram import F
from aiogram import Router
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from aiogram.types import Message

from app.backend.db.models.action import ButtonsEnum
from app.frontend.clients.request_clients import RequestClients
from app.frontend.clients.telegram import TelegramClient
from app.frontend.common.dto.user import CreateUser
from app.frontend.common.dto.user import User
from app.frontend.tg_bot.keyboards.menu import get_menu_keyboard
from app.frontend.tg_bot.keyboards.settings import get_settings_keyboard
from app.frontend.tg_bot.misc.callbacks import Callback
from app.frontend.tg_bot.misc.callbacks import CallbackActions
from app.frontend.tg_bot.misc.states import FSMStates
from app.frontend.vk_bot.misc.constants import HIGHEST_GROUP_NUMBER
from app.frontend.vk_bot.misc.constants import LOWEST_GROUP_NUMBER
from app.frontend.vk_bot.misc.constants import NOT_EXISTING_GROUPS
from config import settings

settings_router = Router()


@settings_router.callback_query(Callback.filter(F.action.in_({CallbackActions.settings})))
async def send_settings(query: CallbackQuery, current_user: User) -> None:
    await query.answer(settings.TELEGRAM_EMPTY_MESSAGE)

    await TelegramClient.send_message(
        query=query,
        text=f"Настройки\n\nТекущая группа: {current_user.group_number}",
        reply_markup=get_settings_keyboard(),
    )

    await RequestClients.tg_backend.mark_action(
        user_id=current_user.id,
        button_name=ButtonsEnum.settings,
    )


@settings_router.callback_query(Callback.filter(F.action.in_({CallbackActions.uptime})))
async def get_uptime(query: CallbackQuery, current_user: User) -> None:
    uptime = await RequestClients.tg_backend.get_last_updated_at()

    try:
        await TelegramClient.send_message(
            query=query,
            text=f"{query.message.text}\n\nРасписание последний раз обновлялось в: {uptime}",
            reply_markup=get_settings_keyboard(),
        )
    except TelegramBadRequest as e:
        if "message is not modified" in e.message:
            pass
        else:
            raise e

    await query.answer(text=f"Последнее обновление было в {uptime}")
    await RequestClients.tg_backend.mark_action(
        user_id=current_user.id,
        button_name=ButtonsEnum.settings,
    )


@settings_router.callback_query(Callback.filter(F.action.in_({CallbackActions.change_group})))
async def change_group(query: CallbackQuery, current_user: User, state: FSMContext) -> None:
    await state.set_state(FSMStates.picking_group)

    await TelegramClient.send_message(query=query, text="Теперь напиши номер своей группы")

    await RequestClients.tg_backend.mark_action(
        user_id=current_user.id,
        button_name=ButtonsEnum.change_group,
    )
    await query.answer(settings.TELEGRAM_EMPTY_MESSAGE)


@settings_router.message(state=FSMStates.picking_group)
async def set_group(message: Message, state: FSMContext) -> None:
    is_digit = message.text.isdigit()

    if not is_digit:
        await TelegramClient.bot.send_message(
            chat_id=message.chat.id, text=f"Напиши цифру, а не {message.text}"
        )
        return

    group_number = int(message.text)

    if group_number in NOT_EXISTING_GROUPS:
        await TelegramClient.bot.send_message(
            chat_id=message.chat.id, text="Такой группы не существует"
        )
        return

    if group_number < LOWEST_GROUP_NUMBER or group_number > HIGHEST_GROUP_NUMBER:
        text = "Врёшь... Таких групп не существует \n\nПринимаются цифры от 100 до 600"
        await TelegramClient.bot.send_message(
            chat_id=message.chat.id,
            text=text,
        )
        return

    user = await RequestClients.tg_backend.update_user(
        data=CreateUser(
            telegram_id=message.from_user.id,
            group_number=group_number,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
        )
    )

    await TelegramClient.bot.send_message(
        chat_id=message.chat.id,
        text=f"Выбрана группа: {user.group_number}",
        reply_markup=get_menu_keyboard(),
    )

    await state.clear()
