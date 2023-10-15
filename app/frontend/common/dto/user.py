from typing import Optional

from pydantic import BaseModel

from app.backend.api.routes.dto.classes.response import ClassScheme
from app.backend.api.services.dto.classes import ClassesEnum
from app.backend.api.services.dto.classes import LinePositionEnum
from app.backend.api.services.dto.classes import WeekDaysEnum


class DayRequest(BaseModel):
    group_number: int
    week_day: WeekDaysEnum
    line_position: LinePositionEnum
    next_week: bool
    user_id: int
    pattern: Optional[str]

    class Config:
        use_enum_values = True


class CreateUser(BaseModel):
    telegram_id: Optional[int]
    vk_id: Optional[int]
    group_number: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]


class User(BaseModel):
    id: int
    telegram_id: Optional[int]
    vk_id: Optional[int]
    group_number: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]


class DaySchema(BaseModel):
    first_class: Optional[ClassScheme]
    second_class: Optional[ClassScheme]
    third_class: Optional[ClassScheme]
    fourth_class: Optional[ClassScheme]
    fifth_class: Optional[ClassScheme]
    fifth_class2: Optional[ClassScheme]
    sixth_class: Optional[ClassScheme]

    def __str__(self):
        prettify = lambda x: x.replace("-", " - ").replace(".", ":")  # noqa
        wrap = lambda x: f"\n{x.value}\n" if x else ""  # noqa

        text = (
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

        if self.fifth_class2:
            text += f"[{prettify(ClassesEnum.FIFTH_CLASS2)}]:\n\n" f"{wrap(self.fifth_class2)}\n"

        if self.sixth_class:
            text += f"[{prettify(ClassesEnum.SIXTH_CLASS)}]:\n\n" f"{wrap(self.sixth_class)}\n"

        return text
