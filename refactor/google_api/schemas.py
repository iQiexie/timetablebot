from typing import Optional, List
from pydantic import Field
from refactor.base.schema import BaseSchema


class ColumnSchema(BaseSchema):
    group_index: int
    rows: List[str]


class CredentialSchema(BaseSchema):
    service_name: str
    credentials: str
