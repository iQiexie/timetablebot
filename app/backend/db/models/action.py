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
from app.backend.db.models.user import ExternalUserModel


class ButtonsEnum(StrEnum):
    statistics_daily_users = "statistics_daily_users"
    current_week = "current_week"
    next_week = "next_week"
    current_week_pattern = "current_week_pattern"
    next_week_pattern = "next_week_pattern"
    pattern_mode = "pattern_mode"
    change_group = "change_group"
    detailed_search = "detailed_search"
    kill_keyboard = "kill_keyboard"
    settings = "settings"
    chat_gpt = "chat_gpt"
    uptime = "uptime"
    menu = "menu"
    back = "back"


class ActionsEnum(StrEnum):
    search = "search"
    search_webapp = "search_webapp"
    search_pattern = "search_pattern"
    search_pattern_webapp = "search_pattern_webapp"
    change_settings = "change_group"
    rate = "rate"
    button_clicked = "button_clicked"


class UserActionModel(Base):
    __tablename__ = "users_activity"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("external_users.id", ondelete="SET NULL"), index=True, nullable=False
    )

    created_at = Column(DateTime, default=datetime.utcnow)
    action = Column(String)
    requested_day = Column(Date)
    new_group = Column(Integer)
    current_group = Column(Integer)
    pattern = Column(String)
    correct = Column(Boolean)
    button = Column(String)
    source = Column(String)

    user = relationship(ExternalUserModel, viewonly=True)


class UsersActivityLegacy(Base):
    __tablename__ = "users_activity_legacy"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(DateTime)
    user_count = Column(Integer)
