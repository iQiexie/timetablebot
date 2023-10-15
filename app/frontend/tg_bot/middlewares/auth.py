from typing import Any
from typing import Awaitable
from typing import Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram.types import Message

from app.frontend.clients.request_clients import RequestClients
from app.frontend.clients.telegram import TelegramClient
from app.frontend.common.dto.user import CreateUser
from config import settings


class AuthMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        pass

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: dict[str, Any],
    ) -> Any:
        subscriber_status = await TelegramClient.bot.get_chat_member(
            chat_id=settings.TELEGRAM_BLOG_CHANNEL_ID,
            user_id=event.from_user.id,
        )

        if subscriber_status.status not in ("creator", "member"):
            subscribe_to_me = (
                "К сожалению, ты не мой подписчик 🥺 "
                "А этот бот был создан только для них.. какое совпадение\n\n"
                "Но у меня есть хорошие новости! Ты тоже можешь подписаться на мой личный "
                "канал, a потом воспользоваться ботом 👀 @not_romaa"
            )

            await TelegramClient.bot.send_message(chat_id=event.from_user.id, text=subscribe_to_me)

            return

        user = await RequestClients.tg_backend.get_user(
            data=CreateUser(
                telegram_id=event.from_user.id,
                first_name=event.from_user.first_name,
                last_name=event.from_user.last_name,
                username=event.from_user.username,
            )
        )

        data["current_user"] = user

        return await handler(event, data)
