from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy.orm import declared_attr
from sqlalchemy.sql.functions import current_timestamp


class TimeMixin:
    @declared_attr
    def __tablename__(cls):  # noqa
        return cls.__name__.lower()

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=current_timestamp().op("AT TIME ZONE")("UTC"))
