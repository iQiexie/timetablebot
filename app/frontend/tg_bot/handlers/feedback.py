import urllib.parse
from datetime import datetime

from aiogram import F
from aiogram import Router
from aiogram.types import CallbackQuery

from app.backend.api.routes.dto.classes.request import RateRequest
from app.frontend.clients.telegram import TelegramClient
from app.frontend.tg_bot.keyboards.feedback import get_empty_feedback_keyboard
from app.frontend.tg_bot.misc.callbacks import Callback
from app.frontend.tg_bot.misc.callbacks import CallbackActions
from app.frontend.vk_bot.misc.request_clients import RequestClients
from config import settings

feedback_router = Router()


@feedback_router.callback_query(Callback.filter(F.action.in_({CallbackActions.downvote})))
async def downvote(query: CallbackQuery, callback_data: Callback) -> None:

    payload = urllib.parse.parse_qs(callback_data.data)
    requested_date = datetime.fromtimestamp(float(payload["s"][0]))
    pattern = payload.get("p")[0] if payload.get("p") else None

    answer_text = (
        "Жалко, что пары пришли неправильные 🥺\n\n"
        "Я не могу просматривать сообщения в телеграм боте, и "
        "поэтому не смогу тебе ответить в этом диалоге\n\n"
        "Напиши, пожалуйста, мне сюда @iqiexie что пошло не так"
    )

    await TelegramClient.send_message(
        query=query,
        text=f"{query.message.text}\n\n{answer_text}",
        reply_markup=get_empty_feedback_keyboard(
            back=CallbackActions.menu,
        ),
    )

    await RequestClients.backend.rate_class(
        data=RateRequest(
            date=requested_date,
            correct=False,
            telegram_id=query.from_user.id,
            pattern=pattern,
        )
    )

    # await TelegramClient.send_message(
    #     query=query,
    #     text=f"{query.message.text}\n\n👎 Неправильно",
    #     reply_markup=get_empty_feedback_keyboard()
    # )

    await query.answer(settings.TELEGRAM_EMPTY_MESSAGE)


@feedback_router.callback_query(Callback.filter(F.action.in_({CallbackActions.upvote})))
async def upvote(query: CallbackQuery, callback_data: Callback) -> None:
    payload = urllib.parse.parse_qs(callback_data.data)
    requested_date = datetime.fromtimestamp(float(payload["s"][0]))
    pattern = payload.get("p")[0] if payload.get("p") else None

    await query.answer("Обратная связь учтена. Спасибо 💖")

    await TelegramClient.send_message(
        query=query,
        text=f"{query.message.text}\n\n👍 Правильно",
        reply_markup=get_empty_feedback_keyboard(
            back=CallbackActions.menu,
        ),
    )

    await RequestClients.backend.rate_class(
        data=RateRequest(
            date=requested_date,
            correct=True,
            telegram_id=query.from_user.id,
            pattern=pattern,
        )
    )
