from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.functions import current_timestamp

from app.backend.db.base_model import Base
from app.backend.db.mixins import TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    vk_id: Mapped[int] = Column(Integer)
    group_index: Mapped[int] = Column(Integer)
    ai_companion_enabled: Mapped[bool] = Column(Boolean, default=False)
    last_activity: Mapped[datetime] = Column(DateTime, default=current_timestamp())


class UsersActivity(Base):
    __tablename__ = "users_activity"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date: Mapped[datetime] = Column(DateTime, default=current_timestamp())
    user_count: Mapped[int] = Column(Integer, nullable=False)

    def __str__(self):
        return f'{self.date.strftime("%d.%m.%Y %H:%M")}: {self.user_count}\n'
