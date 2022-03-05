from sqlalchemy import Column, Integer, String
from refactor.base.db import Base, TimestampMixin


class Class(Base, TimestampMixin):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)

    absolute_index = Column(Integer, unique=True)  # индекс дня в двух неделях. Чётный пн = 0, Нечётный пн = 7
    group_id = Column(Integer)
    text = Column(String(255))
    links = Column(String(255), nullable=True)
