from sqlalchemy import Column, Integer, String, Boolean

from refactor.base.db import Base, BaseMixin, TimestampMixin


class Class(Base, BaseMixin, TimestampMixin):
    __tablename__ = "classes"

    absolute_index = Column(Integer, unique=True)  # индекс дня в двух неделях. Чётный пн = 0, Нечётный пн = 7
    group_id = Column(Integer)
    text = Column(String(255))
    links = Column(String(255), nullable=True)
