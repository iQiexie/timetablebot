from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    class Config:
        orm_mode = True

    uuid: UUID
    vk_id: str
    group_index: int | None
    ai_companion_enabled: bool
    last_activity: datetime
