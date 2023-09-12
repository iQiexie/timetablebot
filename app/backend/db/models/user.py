from sqlalchemy import Column, Integer, String

from app.backend.db.base_model import Base
from app.backend.db.mixins import TimeMixin


class UserModel(TimeMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String, nullable=False)
    source = Column(String, nullable=False)


class ExternalUserModel(TimeMixin, Base):
    __tablename__ = "external_users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True)
    vk_id = Column(Integer, unique=True)
    group_number = Column(Integer)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
