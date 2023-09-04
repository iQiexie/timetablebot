from typing import Optional

from pydantic import BaseModel


class CreateUser(BaseModel):
    telegram_id: Optional[int]
    vk_id: Optional[int]
    group_number: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]


class User(BaseModel):
    id: int
    telegram_id: Optional[int]
    vk_id: Optional[int]
    group_number: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
