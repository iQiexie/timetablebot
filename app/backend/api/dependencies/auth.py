import logging

from fastapi import Depends
from jose import ExpiredSignatureError, JWTError, jwt

from app.backend.api.routes.auth import oauth2_scheme
from app.backend.api.routes.dto.user.response import UserOut
from app.backend.core.exceptions.http_exceptions import InvalidCredentials
from app.backend.db.repos.user import UserRepo
from config import settings


def validate_decode_token(token: str) -> dict:
    if token == settings.ADMIN_SECRET_KEY:
        return {"sub": "admin"}

    try:
        payload = jwt.decode(
            token=token,
            key=settings.JWT_SECRET,
            algorithms=["HS256"],
        )
    except ExpiredSignatureError:
        raise InvalidCredentials(msg="Token has expired")
    except JWTError as e:
        logging.debug(f"JWT decoding error: {e}")
        raise InvalidCredentials(msg="Could not decode JWT token")

    return payload


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    users: UserRepo = Depends(UserRepo),
) -> UserOut:
    payload = validate_decode_token(token=token)

    username = payload.get("sub")
    if username is None:
        raise InvalidCredentials(msg="Auth token is invalid")

    async with users.transaction():
        user = await users.base_get_one(username=username)

    if user is None:
        raise InvalidCredentials(msg="User doesn't exist")

    return user
