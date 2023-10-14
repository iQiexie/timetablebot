import urllib.parse

from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.frontend.tg_bot.misc.callbacks import Callback
from app.frontend.tg_bot.misc.callbacks import CallbackActions


def get_week_keyboard(next_week: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    week = "next" if next_week else "this"
    raw_payload = {"w": week}

    builder.add(
        InlineKeyboardButton(
            text="Понедельник",
            callback_data=Callback(
                action=CallbackActions.by_day, data=urllib.parse.urlencode({"d": 1} | raw_payload)
            ).pack(),
        ),
        InlineKeyboardButton(
            text="Вторник",
            callback_data=Callback(
                action=CallbackActions.by_day, data=urllib.parse.urlencode({"d": 2} | raw_payload)
            ).pack(),
        ),
    )

    builder.row(
        InlineKeyboardButton(
            text="Среда",
            callback_data=Callback(
                action=CallbackActions.by_day, data=urllib.parse.urlencode({"d": 3} | raw_payload)
            ).pack(),
        ),
        InlineKeyboardButton(
            text="Четверг",
            callback_data=Callback(
                action=CallbackActions.by_day, data=urllib.parse.urlencode({"d": 4} | raw_payload)
            ).pack(),
        ),
    )

    builder.row(
        InlineKeyboardButton(
            text="Пятница",
            callback_data=Callback(
                action=CallbackActions.by_day, data=urllib.parse.urlencode({"d": 5} | raw_payload)
            ).pack(),
        ),
        InlineKeyboardButton(
            text="Суббота",
            callback_data=Callback(
                action=CallbackActions.by_day, data=urllib.parse.urlencode({"d": 6} | raw_payload)
            ).pack(),
        ),
    )

    builder.row(
        InlineKeyboardButton(
            text="👇 Назад",
            callback_data=Callback(action=CallbackActions.detailed).pack(),
        ),
    )

    return builder.as_markup()
