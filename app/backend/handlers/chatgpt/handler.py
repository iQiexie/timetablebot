from collections import OrderedDict
from enum import Enum
from typing import List
from typing import Optional

import aiohttp

from app.backend.handlers.chatgpt.redis import ChatGptREDIS
from app.backend.handlers.chatgpt.schemes import ChatGPTChoice
from app.backend.handlers.chatgpt.schemes import ChatGPTResponse
from app.backend.handlers.chatgpt.schemes import UserMessage
from app.backend.handlers.chatgpt.strings import initial_system_message
from config import settings


class TranslationStatusesEnum(str, Enum):
    default = "test"
    context_length = "context_length"


def _translate_errors(message: str) -> ChatGPTResponse:
    if "Rate limit reached" in message:
        status = TranslationStatusesEnum.default
        response_txt = (
            "К сожалению, ChatGPT не может сейчас выполнить твой запрос.\n\n"
            "На текущий момент для этого бота действует ограничение в 20 запросов в "
            "минуту. Попробуй подождать минуту и повторить запрос снова, спасибо за понимание"
        )
    elif "That model is currently overloaded with other requests" in message:
        status = TranslationStatusesEnum.default
        response_txt = (
            "К сожалению, ChatGPT не может сейчас выполнить твой запрос.\n\n"
            "Сервера компании OpenAI (которая создала ChatGPT) на данный момент, к сожалению, "
            "перегружены. Попробуй повторить свой запрос позже, минут через 5-10"
        )
    elif "This model's maximum context length" in message:
        status = TranslationStatusesEnum.context_length
        response_txt = (
            "К сожалению, ChatGPT не может сейчас выполнить твой запрос. \n\n"
            "Сообщение, которое сгенерировал ChatGPT оказалось слишком длинным( "
            "Попробуй спросить у него что-нибудь другое или переформулировать запрос\n\n"
            "Такое часто случается из-за долгого диалога с ChatGPT. Попробуй удалить диалог, нажав "
            "на соответствующую кнопочку в меню"
        )
    else:
        status = TranslationStatusesEnum.default
        response_txt = (
            "К сожалению, ChatGPT не может сейчас выполнить твой запрос. \n\n" f"Причина: {message}"
        )

    return ChatGPTResponse(
        id="1",
        object=status,
        created=1,
        model="mdoel",
        choices=[ChatGPTChoice(message=UserMessage(role="assistant", content=response_txt))],
    )


async def _send_request(messages: list[UserMessage]) -> ChatGPTResponse:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.CHAT_GPT_TOKEN}",
    }

    payload = dict(
        url="https://api.openai.com/v1/chat/completions",
        headers=headers,
        json={"model": "gpt-3.5-turbo", "messages": [msg.dict() for msg in messages]},
    )

    async with aiohttp.ClientSession() as session:
        async with session.post(**payload) as resp:
            resp_json = await resp.json()
            try:
                response = ChatGPTResponse.parse_obj(resp_json)
            except:  # noqa
                message = resp_json.get("error", resp_json).get("message", resp_json)
                response = _translate_errors(message=message)

        print(f'Got response from ChatGPT: {response}')
        return response


async def _save_response(vk_id: int, prompt: str, reply: ChatGPTResponse, redis: ChatGptREDIS):
    message = reply.choices[0].message.content
    role = reply.choices[0].message.role

    if not prompt == "initial":
        await redis.append_message(vk_id=vk_id, message=prompt, role="user")

    await redis.append_message(vk_id=vk_id, message=message, role=role)
    return message


def _convert_history(history: OrderedDict[str, str]) -> List[UserMessage]:
    result = []
    for key_value in list(history.items()):
        role = key_value[0].split(":")[-1]
        message = key_value[1]
        result.append(UserMessage(role=role, content=message))

    return result


async def delete_context(vk_id: int):
    redis = ChatGptREDIS()
    await redis.delete_history(vk_id=vk_id)


async def start_chat(
    vk_id: int,
    redis: ChatGptREDIS,
    conversation_opener: str = None,
) -> Optional[str]:
    history = await redis.get_history(vk_id=vk_id)
    if history:
        return None

    resp = await _send_request([UserMessage(role="system", content=initial_system_message)])
    await _save_response(vk_id=vk_id, reply=resp, redis=redis, prompt="initial")

    message = conversation_opener or "Привет"
    resp = await _send_request([UserMessage(role="user", content=message)])
    message = await _save_response(vk_id=vk_id, prompt=message, reply=resp, redis=redis)
    return message


async def send_message(vk_id: int, message: str) -> str:
    print(f"Sending to ChatGPT message: {message}")
    redis = ChatGptREDIS()
    if initial := await start_chat(vk_id=vk_id, redis=redis):
        return initial

    history_raw = await redis.get_history(vk_id=vk_id)
    history = _convert_history(history=history_raw)
    history.append(UserMessage(role="user", content=message))

    resp = await _send_request(history)

    if resp.object == TranslationStatusesEnum.context_length:
        await delete_context(vk_id=vk_id)
        return await send_message(vk_id=vk_id, message=message)

    message = await _save_response(vk_id=vk_id, prompt=message, reply=resp, redis=redis)
    return message
