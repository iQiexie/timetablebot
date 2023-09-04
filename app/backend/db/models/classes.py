from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint

from app.backend.db.base_model import Base
from app.backend.db.mixins import TimeMixin


class ClassModel(TimeMixin, Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    group_number = Column(Integer, index=True, nullable=False)
    week_day = Column(String, nullable=False)
    line_position = Column(String, nullable=False)
    duration = Column(String, nullable=False)
    row_index = Column(Integer, nullable=False)
    value = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "group_number",
            "week_day",
            "line_position",
            "duration",
            "row_index",
        ),
    )
