from typing import Optional, List, Any
from pydantic import Field
from refactor.backend.base.schema import BaseSchema


class HyperlinkSchema(BaseSchema):
    class_id: int | None
    hyperlink: str | None


class MetaInfoSchema(BaseSchema):
    hyperlinks: List[dict] | None
    class_column: List[str]
    grade: int
    group_id: int


class ClassSchema(BaseSchema):
    week_day_index: int
    above_line: bool
    group_id: int
    index: int  # какая пара по счёту в этом дне, начиная с 1
    text: Optional[Any] = Field(default=None)
    hyperlinks: Optional[Any] = Field(default=None)


class DaySchema(BaseSchema):
    week_day_index: int
    above_line: bool
    group_id: int
    classes: List[Any]
    hyperlinks: Optional[List[Any]] = Field(default=[])
