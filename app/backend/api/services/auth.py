from datetime import datetime
from datetime import timedelta
from functools import lru_cache

from jose import jwt
from passlib.context import CryptContext

from app.backend.api.routes.dto.auth.request import TokenModel
from app.backend.core.exceptions.http_exceptions import InvalidCredentials
from app.backend.db.repos.user import UserRepo
from config import settings


@lru_cache
class SecurityService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                **{settings.SECRET_MEASUREMENT_UNIT: settings.SECRET_EXPIRATION_TIME}
            )

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            claims=to_encode,
            key=settings.JWT_SECRET,
            algorithm="HS256",
        )
        return encoded_jwt

    async def authenticate(
        self,
        username: str,
        password: str,
        users: UserRepo,
    ) -> TokenModel:
        async with users.transaction():
            user = await users.base_get_one(username=username)

        if not user:
            raise InvalidCredentials(msg="Incorrect username or password")

        valid_password = self.verify_password(password, user.password)
        if not valid_password:
            raise InvalidCredentials(msg="Incorrect username or password")

        token = self.create_access_token(data={"sub": user.username})
        return TokenModel(access_token=token, token_type="bearer")  # noqa
