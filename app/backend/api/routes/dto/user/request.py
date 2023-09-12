from typing import Optional

from pydantic import BaseModel, Field


class UserIn(BaseModel):
    username: str
    password: str


class ExternalUserUpdate(BaseModel):
    group_number: int = Field(..., ge=100, lt=600)
    telegram_id: Optional[int]
    vk_id: Optional[int]


class ExternalUserCreate(BaseModel):
    telegram_id: Optional[int]
    vk_id: Optional[int]
    group_number: Optional[int] = Field(None, ge=100, lt=600)
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
