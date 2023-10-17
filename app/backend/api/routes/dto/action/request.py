from typing import Optional

from pydantic import BaseModel

from app.backend.db.models.action import ButtonsEnum


class ButtonActionRequest(BaseModel):
    button: ButtonsEnum
    user_id: int
    pattern: Optional[str]


class ButtonActionPromptRequest(BaseModel):
    user_id: int
    pattern: str
    vk_id: Optional[int]
    telegram_id: Optional[int]
