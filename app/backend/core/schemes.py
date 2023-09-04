from enum import Enum

from pydantic import BaseModel


class BaseModelORM(BaseModel):
    class Config:
        orm_mode = True


class StrEnum(str, Enum):
    def __repr__(self) -> str:
        return str.__repr__(self.value)


class SuccessResponse(BaseModel):
    success: bool
