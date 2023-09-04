from app.backend.core.schemes import BaseModelORM


class TokenModel(BaseModelORM):
    access_token: str
    token_type: str
