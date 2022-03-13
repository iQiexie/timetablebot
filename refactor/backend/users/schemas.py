from refactor.backend.base.schema import BaseSchema
from datetime import datetime

from refactor.backend.users.models import MessageType, MessageIntent


class UserSchema(BaseSchema):
    vk_id: str
    group_index: int | None
    ai_companion_enabled: bool
    last_activity: datetime


class UserMessageSchema(BaseSchema):
    message_type: MessageType
    message_intent = MessageIntent
