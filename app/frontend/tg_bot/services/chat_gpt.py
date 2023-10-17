from asyncio import exceptions
from typing import AsyncIterator

from app.frontend.clients.chat_gpt import FailEnum
from app.frontend.clients.chat_gpt import GPTApi
from app.frontend.clients.chat_gpt import GPTMessage
from app.frontend.clients.key_manager import gpt_keys_manager
from app.frontend.clients.telegram import TelegramClient
from config import settings


async def _get_completion(key: str, context: list[GPTMessage]) -> AsyncIterator[GPTMessage]:
    client = GPTApi(token=key)
    async for response in client.stream_completions(context=context):
        if response.failed_reason not in (FailEnum.key_expired, FailEnum.rate_limit):
            yield GPTMessage(role=response.role, content=response.content)
        else:
            await TelegramClient.bot.send_message(
                chat_id=settings.TELEGRAM_ADMIN,
                text=(
                    f"Key expired: {key}, left: {gpt_keys_manager.keys_count()}\n\n"
                    f"Current keys: {gpt_keys_manager.get_keys()}"
                ),
            )
            key = gpt_keys_manager.get_key()
            async for completion in _get_completion(key=key, context=context):
                yield completion


async def get_completion(context: list[GPTMessage]) -> AsyncIterator[GPTMessage]:
    key = gpt_keys_manager.get_key()
    if not key:
        await TelegramClient.bot.send_message(
            chat_id=settings.TELEGRAM_ADMIN,
            text="All the keys are expired!!!",
        )

        yield GPTMessage(
            role="function",
            content=(
                "К сожалению, чатом сейчас пользуется слишком много людей, лимит "
                "запросов на текущие 5 минут исчерпан 😔. Попробуй ещё раз через 5 минут"
            ),
        )

        return

    try:
        async for completion in _get_completion(key=key, context=context):
            yield completion
    except exceptions.TimeoutError:
        yield GPTMessage(
            role="function",
            content="Прости, твой запрос оказался слишком сложным и не поместился в сообщение 🥲",
        )
        return
