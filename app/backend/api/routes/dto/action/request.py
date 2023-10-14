from typing import Optional

from pydantic import BaseModel

from app.backend.db.models.action import ButtonsEnum


class ButtonActionRequest(BaseModel):
    button: ButtonsEnum
    user_id: int
    pattern: Optional[str]
    source: str
