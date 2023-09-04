from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class SheetUri(BaseModel):
    uri: str


class SheetLink(BaseModel):
    link: Optional[SheetUri]


class TextFormatRuns(BaseModel):
    format: Optional[SheetLink]


class SheetValue(BaseModel):
    formatted_value: Optional[str] = Field(alias="formattedValue")
    text_format_runs: Optional[List[TextFormatRuns]] = Field(alias="textFormatRuns")


class SheetRows(BaseModel):
    values: Optional[List[SheetValue]]


class Sheet(BaseModel):
    rowData: List[SheetRows]
