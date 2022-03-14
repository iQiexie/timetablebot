import sqlalchemy
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql.functions import current_timestamp

from config import settings

engine = create_async_engine(settings.db_url, future=True, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

metadata = sqlalchemy.MetaData()
Base = declarative_base(metadata=metadata)


class TimestampMixin(object):
    created_at = Column(DateTime, default=current_timestamp())
    updated_at = Column(DateTime, onupdate=current_timestamp())
