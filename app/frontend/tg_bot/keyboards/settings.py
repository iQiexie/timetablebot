from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.frontend.tg_bot.misc.callbacks import Callback
from app.frontend.tg_bot.misc.callbacks import CallbackActions


def get_change_group_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="⚙️ Установить группу",
            callback_data=Callback(action=CallbackActions.change_group).pack(),
        )
    )

    return builder.as_markup()


def get_settings_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="👨‍👩‍👧‍👦 Поменять группу",
            callback_data=Callback(action=CallbackActions.change_group).pack(),
        ),
        InlineKeyboardButton(
            text="⚙ Uptime расписания",
            callback_data=Callback(action=CallbackActions.uptime).pack(),
        ),
    )

    # builder.row(
    #     InlineKeyboardButton(
    #         text="📈 Статистика",
    #         callback_data=Callback(action=CallbackActions.statistics).pack(),
    #     ),
    # )

    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=Callback(action=CallbackActions.menu).pack(),
        ),
        InlineKeyboardButton(
            text="Удалить сообщение",
            callback_data=Callback(action=CallbackActions.suicide).pack(),
        ),
    )

    return builder.as_markup()
