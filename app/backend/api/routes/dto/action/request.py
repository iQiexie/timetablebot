from typing import Optional

from pydantic import BaseModel


class ButtonActionRequest(BaseModel):
    button_name: str
    vk_id: Optional[int]
    telegram_id: Optional[int]
    pattern: Optional[str]
