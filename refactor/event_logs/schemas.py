from typing import Optional
from pydantic import Field
from refactor.base.schema import BaseSchema


class EventLogSchema(BaseSchema):
    user_id: Optional[str] = Field(default=None)
    data: str
