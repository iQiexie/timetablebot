from typing import Optional
from pydantic import Field
from refactor.base.schema import BaseSchema


class ClassSchema(BaseSchema):
    absolute_index: int
    group_id: int
    text: str
    links: Optional[str] = Field(default=None)
