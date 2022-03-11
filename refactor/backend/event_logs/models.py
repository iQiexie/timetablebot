import enum
from sqlalchemy import Column, Integer, String, Enum

from refactor.backend.base.db import Base, TimestampMixin


class EventLogType(enum.Enum):
    CREATE = 'CREATE'
    READ = 'READ'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    UNDEFINED = 'UNDEFINED'


class EventLogAction(enum.Enum):
    SPREADSHEET = 'SPREADSHEET'
    CLASS = 'CLASS'
    OTHER = 'OTHER'


class EventLog(Base, TimestampMixin):
    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(String(255), nullable=True)
    data = Column(String(255))
    event_type = Column(Enum(EventLogType), default=EventLogType.UNDEFINED)
    event_action = Column(Enum(EventLogAction), default=EventLogAction.OTHER)
