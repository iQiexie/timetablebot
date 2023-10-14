from aiogram.types import CallbackQuery

from app.frontend.clients.telegram import TelegramClient
from app.frontend.dto.user import User
from app.frontend.tg_bot.keyboards.settings import get_change_group_keyboard


async def group_index_set(message: CallbackQuery, user: User) -> bool:
    if not user.group_number:
        text = "Пожалуйста, укажи группу. Для этого нажми на кнопку внизу 👇"
        await TelegramClient.bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=message.message.message_id,
            text=text,
            reply_markup=get_change_group_keyboard(),
        )
        return False

    return True
