from typing import Optional

from app.backend.core.schemes import BaseModelORM


class UserOut(BaseModelORM):
    id: int
    username: str


class ExternalUser(BaseModelORM):
    id: int
    gpt_allowed: Optional[bool]
    telegram_id: Optional[int]
    vk_id: Optional[int]
    group_number: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
