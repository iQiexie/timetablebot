from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.frontend.tg_bot.misc.callbacks import Callback
from app.frontend.tg_bot.misc.callbacks import CallbackActions


def get_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="🔎 Сегодняшние пары",
            callback_data=Callback(action=CallbackActions.today).pack(),
        ),
        InlineKeyboardButton(
            text="🔎 Завтрашние пары",
            callback_data=Callback(action=CallbackActions.tomorrow).pack(),
        ),
    )

    builder.row(
        InlineKeyboardButton(
            text="👀 Подробный поиск",
            callback_data=Callback(action=CallbackActions.detailed).pack(),
        )
    )

    builder.row(
        InlineKeyboardButton(
            text="🛠 Настройки",
            callback_data=Callback(action=CallbackActions.settings).pack(),
        ),
        InlineKeyboardButton(
            text="Удалить сообщение",
            callback_data=Callback(action=CallbackActions.suicide).pack(),
        ),
    )

    return builder.as_markup()


def get_detailed_menu(pattern: str = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text="👈 Эта неделя",
            callback_data=Callback(
                action=CallbackActions.sweak, data=f"this,{pattern or ' '}"
            ).pack(),
        ),
        InlineKeyboardButton(
            text="👉 Следующая неделя",
            callback_data=Callback(
                action=CallbackActions.sweak, data=f"next,{pattern or ' '}"
            ).pack(),
        ),
    )

    if not pattern:
        pattern_search_button_text = "👩‍🏫 Поиск по преподавателю"
        pattern_search_action = CallbackActions.pattern_search
    else:
        pattern_search_button_text = "❌ Сбросить режим поиска"
        pattern_search_action = CallbackActions.stop_pattern_search

    builder.row(
        InlineKeyboardButton(
            text=pattern_search_button_text,
            callback_data=Callback(action=pattern_search_action).pack(),
        ),
    )

    builder.row(
        InlineKeyboardButton(
            text="Меню",
            callback_data=Callback(action=CallbackActions.menu).pack(),
        )
    )

    return builder.as_markup()
