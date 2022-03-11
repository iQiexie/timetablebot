from refactor.backend.base.schema import BaseSchema


class CredentialSchema(BaseSchema):
    service_name: str
    credentials: str
