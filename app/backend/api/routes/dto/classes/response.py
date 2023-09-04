from datetime import date

from app.backend.api.services.dto.classes import ClassesEnum
from app.backend.core.schemes import BaseModelORM


class ClassScheme(BaseModelORM):
    id: int
    duration: ClassesEnum | str
    value: str
    group_number: int
    requested_date: date

    class Config:
        use_enum_values = True
