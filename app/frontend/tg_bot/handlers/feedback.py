import urllib.parse
from datetime import datetime

from aiogram import F
from aiogram import Router
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.backend.api.routes.dto.classes.request import RateRequest
from app.frontend.clients.request_clients import RequestClients
from app.frontend.clients.telegram import TelegramClient
from app.frontend.tg_bot.keyboards.feedback import get_empty_feedback_keyboard
from app.frontend.tg_bot.misc.callbacks import Callback
from app.frontend.tg_bot.misc.callbacks import CallbackActions
from config import settings

feedback_router = Router()


@feedback_router.callback_query(Callback.filter(F.action.in_({CallbackActions.downvote})))
async def downvote(query: CallbackQuery, callback_data: Callback, state: FSMContext) -> None:
    context_data = await state.get_data()
    pattern = context_data.get("pattern")
    if pattern == " ":
        pattern = None

    payload = urllib.parse.parse_qs(callback_data.data)
    requested_date = datetime.fromtimestamp(float(payload["s"][0]))

    answer_text = (
        "Жалко, что пары пришли неправильные 🥺\n\n"
        "Я не могу просматривать сообщения в телеграм боте, и "
        "поэтому не смогу тебе ответить в этом диалоге\n\n"
        "Напиши, пожалуйста, мне сюда @iqiexie что пошло не так\n\n"
    )

    await TelegramClient.send_message(
        message=query.message,
        text=f"{query.message.text}\n\n{answer_text}",
        reply_markup=get_empty_feedback_keyboard(
            back=context_data.get("back"),
            back_payload=context_data.get("back_payload"),
        ),
    )

    await RequestClients.tg_backend.rate_class(
        data=RateRequest(
            date=requested_date,
            correct=False,
            telegram_id=query.from_user.id,
            pattern=pattern,
        )
    )

    await query.answer(settings.TELEGRAM_EMPTY_MESSAGE)


@feedback_router.callback_query(Callback.filter(F.action.in_({CallbackActions.upvote})))
async def upvote(query: CallbackQuery, callback_data: Callback, state: FSMContext) -> None:
    context_data = await state.get_data()
    pattern = context_data.get("pattern")
    payload = urllib.parse.parse_qs(callback_data.data)
    requested_date = datetime.fromtimestamp(float(payload["s"][0]))

    await query.answer("Обратная связь учтена. Спасибо 💖")

    await TelegramClient.send_message(
        message=query.message,
        text=f"{query.message.text}\n\n👍 Правильно",
        reply_markup=get_empty_feedback_keyboard(
            back=context_data.get("back") or CallbackActions.menu,
            back_payload=context_data.get("back_payload"),
        ),
    )

    await RequestClients.tg_backend.rate_class(
        data=RateRequest(
            date=requested_date,
            correct=True,
            telegram_id=query.from_user.id,
            pattern=pattern,
        )
    )
