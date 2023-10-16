from asyncio import exceptions

from app.frontend.clients.chat_gpt import FailEnum
from app.frontend.clients.chat_gpt import GPTApi
from app.frontend.clients.chat_gpt import GPTMessage
from app.frontend.clients.key_manager import gpt_keys_manager
from app.frontend.clients.telegram import TelegramClient
from config import settings


async def get_completion(context: list[GPTMessage]) -> GPTMessage:
    key = gpt_keys_manager.get_key()
    if not key:
        await TelegramClient.bot.send_message(
            chat_id=settings.TELEGRAM_ADMIN,
            text="All the keys are expired!!!",
        )

        return GPTMessage(
            role="function",
            content=(
                "К сожалению, чатом сейчас пользуется слишком много людей, лимит "
                "запросов на текущие 5 минут исчерпан 😔. Попробуй ещё раз через 5 минут"
            ),
        )

    client = GPTApi(token=key)

    try:
        completion = await client.get_completion(context=context)
    except exceptions.TimeoutError:
        return GPTMessage(
            role="function",
            content="Прости, твой запрос оказался слишком сложным и не поместился в сообщение 🥲",
        )

    if completion.failed_reason in (FailEnum.key_expired, FailEnum.rate_limit):
        await TelegramClient.bot.send_message(
            chat_id=settings.TELEGRAM_ADMIN,
            text=(
                f"Key expired: {key}, left: {gpt_keys_manager.keys_count()}\n\n"
                f"Current keys: {gpt_keys_manager.get_keys()}"
            ),
        )
        return await get_completion(context=context)

    return GPTMessage(role=completion.role, content=completion.content)
