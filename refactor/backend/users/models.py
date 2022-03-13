import enum
from uuid import uuid4

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.functions import current_timestamp

from refactor.backend.base.db import Base, TimestampMixin


class MessageType(str, enum.Enum):
    READ = 'READ'
    UPDATE = 'UPDATE'
    UNDEFINED = 'UNDEFINED'


class MessageIntent(str, enum.Enum):
    MONDAY_BELOW = 'MONDAY_BELOW'
    MONDAY_ABOVE = 'MONDAY_ABOVE'
    TUESDAY_BELOW = 'TUESDAY_BELOW'
    TUESDAY_ABOVE = 'TUESDAY_ABOVE'
    WEDNESDAY_BELOW = 'WEDNESDAY_BELOW'
    WEDNESDAY_ABOVE = 'WEDNESDAY_ABOVE'
    THURSDAY_BELOW = 'THURSDAY_BELOW'
    THURSDAY_ABOVE = 'THURSDAY_ABOVE'
    FRIDAY_BELOW = 'FRIDAY_BELOW'
    FRIDAY_ABOVE = 'FRIDAY_ABOVE'
    SATURDAY_BELOW = 'SATURDAY_BELOW'
    SATURDAY_ABOVE = 'SATURDAY_ABOVE'
    SETTINGS = 'SETTINGS'
    GROUP = 'GROUP'
    COMPANION = 'COMPANION'
    UPTIME = 'UPTIME'
    UNDEFINED = 'UNDEFINED'


class User(Base, TimestampMixin):
    __tablename__ = "users"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    vk_id = Column(Integer)
    group_index = Column(Integer, nullable=True)
    ai_companion_enabled = Column(Boolean, default=False)
    last_activity = Column(DateTime, default=current_timestamp())


class UserMessage(Base, TimestampMixin):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    user_uuid = Column(UUID, ForeignKey('users.uuid'))

    message_type = Column(Enum(MessageType), default=MessageType.UNDEFINED)
    message_intent = Column(Enum(MessageIntent), default=MessageIntent.UNDEFINED)
