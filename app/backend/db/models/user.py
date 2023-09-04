from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.backend.core.schemes import StrEnum
from app.backend.db.base_model import Base
from app.backend.db.mixins import TimeMixin


class ActionsEnum(StrEnum):
    search = "search"
    search_pattern = "search_pattern"
    change_settings = "change_group"
    rate = "rate"


class UserModel(TimeMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)


class ExternalUserModel(TimeMixin, Base):
    __tablename__ = "external_users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True)
    vk_id = Column(Integer, unique=True)
    group_number = Column(Integer)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)


class UserActionModel(Base):
    __tablename__ = "users_activity"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("external_users.id", ondelete="SET NULL"), index=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    action = Column(String)
    requested_day = Column(Date)
    new_group = Column(Integer)
    current_group = Column(Integer)
    pattern = Column(String)
    correct = Column(Boolean)

    user = relationship("ExternalUserModel", viewonly=True)
