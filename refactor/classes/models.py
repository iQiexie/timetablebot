from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UnicodeText
from refactor.base.db import Base, TimestampMixin


class Class(Base, TimestampMixin):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)

    week_day_index = Column(Integer)
    above_line = Column(Boolean)
    group_id = Column(Integer)
    text = Column(UnicodeText(length=2000), nullable=True)


class Hyperlink(Base, TimestampMixin):
    __tablename__ = "hyperlinks"

    id = Column(Integer, primary_key=True, index=True)

    class_id = Column(Integer, ForeignKey('classes.id'), nullable=True)
    hyperlink = Column(String(1000), nullable=True)
