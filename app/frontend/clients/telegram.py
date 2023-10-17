import asyncio
import logging
from typing import Optional

from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import Message

from config import settings

logging.info(f"Starting telegram bot with {settings.TELEGRAM_TOKEN}")


class TelegramClient:
    bot = Bot(token=settings.TELEGRAM_TOKEN)

    @classmethod
    async def _delete_message(
        cls,
        message: Message,
        text: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        try:
            await TelegramClient.bot.delete_message(
                chat_id=message.chat.id,
                message_id=message.message_id,
            )

            return await TelegramClient.bot.send_message(
                chat_id=message.chat.id,
                text=text,
                reply_markup=reply_markup,
            )
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after + 1)
            return await cls._delete_message(
                message=message,
                text=text,
                reply_markup=reply_markup,
            )

    @classmethod
    async def _edit_message(
        cls,
        message: Message,
        text: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ):
        try:
            return await TelegramClient.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.message_id,
                text=text,
                reply_markup=reply_markup,
            )
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after + 1)
            return await cls._edit_message(
                message=message,
                text=text,
                reply_markup=reply_markup,
            )

    @classmethod
    async def _send_message(
        cls,
        message: Message,
        text: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ):
        try:
            return await TelegramClient.bot.send_message(
                chat_id=message.from_user.id,
                text=text,
                reply_markup=reply_markup,
            )
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after + 1)
            return await cls._send_message(
                message=message,
                text=text,
                reply_markup=reply_markup,
            )

    @classmethod
    async def send_message(
        cls,
        message: Message,
        text: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        delete_message: bool = False,
        new_message: bool = False,
    ) -> Message:
        if new_message:
            return await cls._send_message(
                message=message,
                text=text,
                reply_markup=reply_markup,
            )

        if delete_message:
            return await cls._delete_message(
                message=message,
                text=text,
                reply_markup=reply_markup,
            )

        return await cls._edit_message(
            message=message,
            text=text,
            reply_markup=reply_markup,
        )
