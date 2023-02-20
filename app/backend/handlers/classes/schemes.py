from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import root_validator
from pydantic.utils import GetterDict

from app.backend.handlers.classes.enums import ClassesEnum

DURATIONS_MAP = {
    "9.00-10.30": "first_class",
    "10.40-12.10": "second_class",
    "12.40-14.10": "third_class",
    "14.20-16.00": "fourth_class",
    "16.00-17-30": "fifth_class",
    "16.00-17.30": "fifth_class",
}


# в DURATIONS_MAP можно добавлять сколько угодно продолжительностей (вроде 16.00-17.30).
# app.backend.handlers.classes.scraper всё равно потом приводит всё к одному формату:
# 16.00-17.30 (часы.минуты-часы.минуты)
# эти продолжительности ещё используются в app.backend.handlers.classes.enums


class DaySchema(BaseModel):
    first_class: Optional[str]
    second_class: Optional[str]
    third_class: Optional[str]
    fourth_class: Optional[str]
    fifth_class: Optional[str]

    @root_validator(pre=True)
    def parse_grades(cls, values: GetterDict):
        result = {}

        for key, value in values.items():
            group_number, week_day, line, duration, row = key.split(":")
            field = DURATIONS_MAP.get(duration)
            result[field] = value

        return result

    def __str__(self):
        prettify = lambda x: x.replace("-", " - ").replace(".", ":")  # noqa
        wrap = lambda x: f"\n{x}\n" if x else ""  # noqa

        return f"""
        [{prettify(ClassesEnum.FIRST_CLASS)}]:
        {wrap(self.first_class)}
        [{prettify(ClassesEnum.SECOND_CLASS)}]:
        {wrap(self.second_class)}
        [{prettify(ClassesEnum.THIRD_CLASS)}]:
        {wrap(self.third_class)}
        [{prettify(ClassesEnum.FOURTH_CLASS)}]:
        {wrap(self.fourth_class)}
        [{prettify(ClassesEnum.FIFTH_CLASS)}]:        
        {wrap(self.fifth_class)}
        """


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
