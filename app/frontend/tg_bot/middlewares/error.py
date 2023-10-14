import traceback
from typing import Any
from typing import Awaitable
from typing import Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram.types import Message


class ErrorMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        pass

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: dict[str, Any],
    ) -> Any:
        try:
            await handler(event, data)
        except Exception as e:
            await event.answer(f"Error occurred\n\n{e}")
            traceback.print_exc()
