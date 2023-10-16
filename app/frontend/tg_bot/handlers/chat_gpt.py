from aiogram import F
from aiogram import Router
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from app.backend.db.models.action import ButtonsEnum
from app.frontend.clients.chat_gpt import GPTMessage
from app.frontend.clients.request_clients import RequestClients
from app.frontend.clients.telegram import TelegramClient
from app.frontend.common.dto.user import User
from app.frontend.tg_bot.keyboards.chat_gpt import get_gpt_menu_keyboard
from app.frontend.tg_bot.keyboards.menu import get_light_menu_keyboard
from app.frontend.tg_bot.misc.callbacks import Callback
from app.frontend.tg_bot.misc.callbacks import CallbackActions
from app.frontend.tg_bot.misc.states import FSMStates
from app.frontend.tg_bot.services.chat_gpt import get_completion
from config import settings

gpt_router = Router()


@gpt_router.callback_query(Callback.filter(F.action.in_({CallbackActions.gpt})))
async def send_menu(query: CallbackQuery, state: FSMContext, current_user: User) -> None:
    await query.answer(settings.TELEGRAM_EMPTY_MESSAGE)
    await TelegramClient.send_message(
        query=query,
        text="🟢 Диалог с ChatGPT активен\n\nПривет, чем могу помочь?",
        reply_markup=get_gpt_menu_keyboard(),
        delete_message=True,
    )

    await state.clear()
    await state.set_state(FSMStates.chat_gpt)
    await RequestClients.tg_backend.mark_action(
        user_id=current_user.id,
        button_name=ButtonsEnum.chat_gpt,
    )


@gpt_router.message(state=FSMStates.chat_gpt)
async def process_message(message: Message, state: FSMContext, current_user: User) -> None:
    if not current_user.gpt_allowed:
        await message.answer(
            text="К сожалению, превышен лимит сообщений (5 раз в минуту)",
            reply_markup=get_light_menu_keyboard(),
        )
        return

    await TelegramClient.bot.send_chat_action(
        chat_id=message.chat.id,
        action="typing",
    )

    msg = await TelegramClient.bot.send_message(
        chat_id=message.chat.id,
        text="Генерирую ответ... ⏳",
    )

    my_name = message.from_user.first_name or message.from_user.username
    state_data = await state.get_data()
    chat_context = state_data.get(
        "chat_context", [{"role": "user", "content": f"Привет, я {my_name}"}]
    )
    chat_context.append({"role": "user", "content": f"{message.text}"})

    response = await get_completion(
        context=[GPTMessage(**c) for c in chat_context],
    )
    chat_context.append(response.dict())

    await TelegramClient.bot.edit_message_text(
        chat_id=msg.chat.id,
        message_id=msg.message_id,
        text=response.content,
        reply_markup=get_light_menu_keyboard(),
    )

    state_data["chat_context"] = chat_context
    await state.set_data(state_data)

    await RequestClients.tg_backend.mark_action(
        user_id=current_user.id,
        button_name=ButtonsEnum.chat_gpt,
        pattern=message.text,
    )
