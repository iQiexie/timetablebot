import logging
from typing import Optional

from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import Message

from config import settings

logging.info(f"Starting telegram bot with {settings.TELEGRAM_TOKEN}")


class TelegramClient:
    bot = Bot(token=settings.TELEGRAM_TOKEN)

    @staticmethod
    async def send_message(
        query: CallbackQuery | Message,
        text: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        if isinstance(query, CallbackQuery):
            return await TelegramClient.bot.edit_message_text(
                chat_id=query.from_user.id,
                message_id=query.message.message_id,
                text=text,
                reply_markup=reply_markup,
            )

        return await TelegramClient.bot.send_message(
            chat_id=query.from_user.id,
            text=text,
            reply_markup=reply_markup,
        )
