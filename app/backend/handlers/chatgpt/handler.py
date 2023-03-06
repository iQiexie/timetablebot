from collections import OrderedDict
from typing import List
from typing import Optional

import aiohttp

from app.backend.handlers.chatgpt.redis import ChatGptREDIS
from app.backend.handlers.chatgpt.schemes import ChatGPTResponse
from app.backend.handlers.chatgpt.schemes import UserMessage
from app.backend.handlers.chatgpt.strings import initial_system_message
from config import settings


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
            return ChatGPTResponse.parse_obj(await resp.json())


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


async def start_chat(
    vk_id: int, redis: ChatGptREDIS, conversation_opener: str = None,
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
    redis = ChatGptREDIS()
    if initial := await start_chat(vk_id=vk_id, redis=redis):
        return initial

    history_raw = await redis.get_history(vk_id=vk_id)
    history = _convert_history(history=history_raw)
    history.append(UserMessage(role="user", content=message))

    resp = await _send_request(history)
    message = await _save_response(vk_id=vk_id, prompt=message, reply=resp, redis=redis)
    return message
