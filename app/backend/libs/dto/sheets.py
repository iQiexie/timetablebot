from typing import List, Optional

from pydantic import BaseModel, Field


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
    row_data: List[SheetRows] = Field(alias="rowData")

    class Config:
        allow_population_by_field_name = True
