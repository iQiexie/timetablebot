from sqlalchemy import MetaData, Column, DateTime, Integer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, declared_attr, declarative_mixin
from sqlalchemy.sql.functions import current_timestamp

from config import settings

engine = create_async_engine(settings.DB_URL, future=True, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base(metadata=MetaData())


class TimestampMixin(object):
    created_at = Column(DateTime, default=current_timestamp())
    updated_at = Column(DateTime, onupdate=current_timestamp())


class BaseMixin(object):
    id = Column(Integer, primary_key=True, index=True)
