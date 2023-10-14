import urllib.parse
from typing import Optional

from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.frontend.tg_bot.misc.callbacks import Callback
from app.frontend.tg_bot.misc.callbacks import CallbackActions


def get_feedback_keyboard(
    searching_date: float, back: CallbackActions, back_payload: Optional[dict] = None
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    raw_payload = {"s": searching_date}
    payload = urllib.parse.urlencode(raw_payload)

    downvote = Callback(action=CallbackActions.downvote, data=payload).pack()
    upvote = Callback(action=CallbackActions.upvote, data=payload).pack()
    back = Callback(
        action=back, data=urllib.parse.urlencode(raw_payload | (back_payload or {}))
    ).pack()

    builder.row(
        InlineKeyboardButton(text="👍 Правильно ", callback_data=upvote),
        InlineKeyboardButton(text="👎 Неправильно", callback_data=downvote),
    )

    builder.row(
        InlineKeyboardButton(text="Назад", callback_data=back),
    )

    return builder.as_markup()


def get_empty_feedback_keyboard(
    back: CallbackActions, back_payload: Optional[dict] = None
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    payload = urllib.parse.urlencode(back_payload or {})

    back = Callback(action=back, data=payload).pack()
    builder.row(InlineKeyboardButton(text="Назад", callback_data=back))

    return builder.as_markup()
