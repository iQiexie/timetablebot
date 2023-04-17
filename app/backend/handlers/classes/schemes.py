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
    "14.20-15.50": "fourth_class",
    "16.00-17-30": "fifth_class",
    "16.00-17.30": "fifth_class",
}


# в DURATIONS_MAP можно добавлять сколько угодно продолжительностей (вроде 16.00-17.30).
# app.backend.handlers.classes.scraper всё равно потом приводит всё к одному формату:
# 16.00-17.30 (часы.минуты-часы.минуты)
# эти продолжительности ещё используются в app.backend.handlers.classes.enums


class ClassSchema(BaseModel):
    value: str
    group: int
    display_group: bool

    def __str__(self):
        if not self.display_group:
            return self.value

        return f"Группа: {self.group}\n\n{self.value}"


class DaySchema(BaseModel):
    first_class: Optional[ClassSchema]
    second_class: Optional[ClassSchema]
    third_class: Optional[ClassSchema]
    fourth_class: Optional[ClassSchema]
    fifth_class: Optional[ClassSchema]

    @root_validator(pre=True)
    def parse_grades(cls, values: GetterDict):
        result = {}
        display_group = values.get("display_group", False)

        for key, value in values.items():
            values = key.split(":")
            if len(values) != 5:  # if not redis key
                continue

            group_number, week_day, line, duration, row = key.split(":")
            field = DURATIONS_MAP.get(duration)
            result[field] = ClassSchema(
                value=value,
                group=group_number,
                display_group=display_group,
            )

        return result

    def __str__(self):
        prettify = lambda x: x.replace("-", " - ").replace(".", ":")  # noqa
        wrap = lambda x: f"\n{x}\n" if x else ""  # noqa

        return (
            f"[{prettify(ClassesEnum.FIRST_CLASS)}]:\n\n"
            f"{wrap(self.first_class)}\n\n"
            f"[{prettify(ClassesEnum.SECOND_CLASS)}]:\n\n"
            f"{wrap(self.second_class)}\n\n"
            f"[{prettify(ClassesEnum.THIRD_CLASS)}]:\n\n"
            f"{wrap(self.third_class)}\n\n"
            f"[{prettify(ClassesEnum.FOURTH_CLASS)}]:\n\n"
            f"{wrap(self.fourth_class)}\n\n"
            f"[{prettify(ClassesEnum.FIFTH_CLASS)}]:\n\n"
            f"{wrap(self.fifth_class)}\n"
        )


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
