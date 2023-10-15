from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.frontend.tg_bot.misc.callbacks import Callback
from app.frontend.tg_bot.misc.callbacks import CallbackActions


def get_gpt_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text="🗑 Новый диалог", callback_data=Callback(action=CallbackActions.gpt).pack()
        ),
        InlineKeyboardButton(
            text="Назад", callback_data=Callback(action=CallbackActions.menu).pack()
        ),
    )

    return builder.as_markup()
