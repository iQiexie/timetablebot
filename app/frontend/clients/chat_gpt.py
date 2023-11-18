import json
import logging
from datetime import datetime
from datetime import timedelta
from enum import Enum
from json import JSONDecodeError
from typing import AsyncIterator
from typing import List
from typing import Optional

from pydantic import BaseModel

from app.base_request_client import BaseRequestsClient
from app.frontend.clients.key_manager import gpt_keys_manager
from config import settings


class FailEnum(str, Enum):
    key_expired = "key_expired"
    rate_limit = "rate_limit"  # слишком много одновременных обращений
    busy = "busy"
    max_context = "max_context"
    unknown = "unknown"


class GPTResponse(BaseModel):
    role: str
    content: str
    failed_reason: Optional[FailEnum]


class GPTMessage(BaseModel):
    role: str
    content: str


class GPTApi(BaseRequestsClient):
    def __init__(self, token: str):
        self.base_url = settings.GPT_PROVIDER_URL
        self.auth = {"Authorization": f"Bearer {token}"}
        self.raise_exceptions = False
        self.token = token
        self.proxy = settings.GPT_PROXY

    def _parse_responses(self, message: str) -> GPTResponse:
        if "Rate limit reached" in message:
            failed_reason = FailEnum.rate_limit

            if " / day" in message:
                available_after = datetime.now() + timedelta(minutes=60)
            elif "/ min" in message:
                available_after = datetime.now() + timedelta(minutes=2)
            else:
                available_after = datetime.now() + timedelta(minutes=30)

            gpt_keys_manager.freeze_key(key=self.token, available_after=available_after)

            response_txt = (
                "К сожалению, ChatGPT не может сейчас выполнить твой запрос.\n\n"
                "На текущий момент для этого бота действует ограничение на количество запросов в "
                "минуту. Попробуй подождать минуту и повторить запрос снова, спасибо за понимание!"
                "\n\n Сейчас доступно 5 сообщений в минуту"
            )
        elif "That model is currently overloaded with other requests" in message:
            failed_reason = FailEnum.busy
            response_txt = (
                "К сожалению, ChatGPT не может сейчас выполнить твой запрос.\n\n"
                "Сервера компании OpenAI (которая создала ChatGPT) на данный момент, к сожалению, "
                "перегружены. Попробуй повторить свой запрос позже, минут через 5-10"
            )
        elif "This model's maximum context length" in message:
            failed_reason = FailEnum.max_context
            response_txt = (
                "К сожалению, ChatGPT не может сейчас выполнить твой запрос. \n\n"
                "Сообщение, которое сгенерировал ChatGPT оказалось слишком длинным( "
                "Попробуй спросить у него что-нибудь другое или переформулировать запрос\n\n"
                "Такое часто случается из-за долгого диалога с ChatGPT. "
                "Попробуй удалить диалог, нажав на соответствующую кнопочку в меню"
            )
        elif "You exceeded your current quota" in message:
            gpt_keys_manager.terminate_key(key=self.token)
            failed_reason = FailEnum.key_expired
            response_txt = (
                "К сожалению, ChatGPT не может выполнить твой запрос. "
                "У админа закончились рабочие ключи, но он скоро их добудет, не переживай!"
            )
        else:
            failed_reason = FailEnum.unknown
            response_txt = (
                "К сожалению, ChatGPT не может сейчас выполнить твой запрос. \n\n"
                f"Причина: {message}"
            )

        return GPTResponse(
            role="function",
            content=response_txt,
            failed_reason=failed_reason,
        )

    @staticmethod
    def _parse_raw_answer(resp: str) -> Optional[dict]:
        if "[DONE]" in resp:
            return

        raw_resp = resp.replace("data: ", "")[:-1]

        if raw_resp in ("\n", '"') or not raw_resp:
            return

        try:
            return json.loads(raw_resp)
        except JSONDecodeError:
            if '"message": "' in resp:
                return {"error": resp.replace('"message": "', "").replace('",\n', "")}

            return

    @staticmethod
    def _prepare_context(context: List[GPTMessage]) -> list[dict]:
        messages_index = set()
        new_context = list()

        # Убираем дубликаты

        for ctx in context:
            if ctx.content not in messages_index:
                messages_index.add(ctx.content)
                new_context.append(ctx)

        # Убираем сообщения бота юзеру
        return [c.dict() for c in new_context if c.role != "function"]

    async def stream_completions(self, context: list[GPTMessage]) -> AsyncIterator[GPTResponse]:
        messages = self._prepare_context(context=context)
        stream_data = dict(
            url="/v1/chat/completions",
            json={"model": "gpt-3.5-turbo", "messages": messages, "stream": True},
        )

        async for resp in self._stream_request(**stream_data):
            data = self._parse_raw_answer(resp=resp)
            if not data:
                continue

            logging.info(f"gpt_debug!! {data=}")
            if errors := data.get("error"):
                yield self._parse_responses(message=errors)
            else:
                message = data["choices"][0]["delta"]
                yield GPTResponse(
                    role=message.get("role", "assistant"),
                    content=message.get("content", ""),
                )
