from sqlalchemy import Column, Integer, String

from refactor.base.db import Base, TimestampMixin


class EventLog(Base, TimestampMixin):
    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(String(255), nullable=True)
    data = Column(String(255))
