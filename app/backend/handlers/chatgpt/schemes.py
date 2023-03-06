from typing import List
from typing import Optional

from pydantic import BaseModel


class UserMessage(BaseModel):
    role: str
    content: str


class History(BaseModel):
    history: list[UserMessage]


class ChatGPTChoice(BaseModel):
    message: UserMessage
    finish_reason: Optional[str]
    index: Optional[int]


class ChatGPTUsageData(BaseModel):
    prompt_tokens: str
    completion_tokens: str
    total_tokens: str


class ChatGPTResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    usage: Optional[ChatGPTUsageData]
    choices: List[ChatGPTChoice]
