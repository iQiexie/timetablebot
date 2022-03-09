from typing import Optional, List
from pydantic import Field
from refactor.base.schema import BaseSchema


class CredentialSchema(BaseSchema):
    service_name: str
    credentials: str
