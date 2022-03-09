from typing import Optional, List, Any, Union
from pydantic import Field
from refactor.base.schema import BaseSchema


class MetaInfoSchema(BaseSchema):
    hyperlinks: List[dict]
    class_column: List[str]
    grade: int
    group_id: int


class ClassSchema(BaseSchema):
    week_day_index: int
    above_line: bool
    group_id: int
    text: str
    hyperlinks: Optional[Any] = Field(default=None)


class DaySchema(BaseSchema):
    week_day_index: int
    above_line: bool
    group_id: int
    classes: List[Any]
    hyperlinks: Optional[List[Any]] = Field(default=[])
