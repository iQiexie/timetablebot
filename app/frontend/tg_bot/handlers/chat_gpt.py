import json

import asyncstdlib as a
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
        message=query.message,
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

    msg = await TelegramClient.bot.send_message(
        chat_id=message.chat.id,
        text="Генерирую ответ... ⏳",
    )

    await TelegramClient.bot.send_chat_action(
        chat_id=message.chat.id,
        action="typing",
    )

    my_name = message.from_user.first_name or message.from_user.username
    state_data = await state.get_data()
    chat_context = state_data.get(
        "chat_context", [{"role": "user", "content": f"Привет, я {my_name}"}]
    )
    chat_context.append({"role": "user", "content": f"{message.text}"})
    context = [GPTMessage(**c) for c in chat_context]

    final_msg = ""
    final_role = "assistant"
    header = "Генерация ответа... ⏳\n\n"

    async for i, response in a.enumerate(get_completion(context=context)):
        if not response.content:
            continue

        final_msg += response.content
        final_role = response.role

        if {
            i > 30 and i % 10 != 0: True,
            i > 100 and i % 20 != 0: True,
        }.get(True):
            continue

        wait = 0 + i / 200
        await TelegramClient.send_message(
            message=msg,
            text=header + final_msg,
            reply_markup=get_light_menu_keyboard(),
            wait=wait if wait < 0.5 else 0.5,
        )

    await TelegramClient.send_message(
        message=msg,
        text=final_msg or "Произошла ошибка :(",
        reply_markup=get_light_menu_keyboard() if final_msg else None,
    )

    if not final_msg:
        return

    chat_context.append({"role": final_role, "content": final_msg})
    state_data["chat_context"] = chat_context
    await state.set_data(state_data)

    await RequestClients.tg_backend.mark_action(
        user_id=current_user.id,
        button_name=ButtonsEnum.chat_gpt,
        pattern=json.dumps(chat_context, ensure_ascii=False),
    )
