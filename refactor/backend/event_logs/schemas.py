from enum import Enum
from typing import Optional
from pydantic import Field
from refactor.backend.base.schema import BaseSchema


class EventLogSchema(BaseSchema):
    user_id: Optional[str] = Field(default=None)
    data: str
    event_type: Enum
    event_action: Enum
