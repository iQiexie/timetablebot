from typing import Any
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel
from starlette import status


class HTTPExceptionDetail(BaseModel):
    error: str
    msg: str
    detail: dict = {}


class BaseHttpException(HTTPException):
    def __init__(
        self,
        error: str,
        msg: str,
        status_code: int,
        detail: dict = None,
        headers: Optional[dict[str, Any]] = None,
    ) -> None:
        if not isinstance(detail, dict):
            detail = dict(detail=detail)

        detail = HTTPExceptionDetail(error=error, msg=msg, detail=detail).json()
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class InvalidCredentials(BaseHttpException):
    error: str = "invalid_credentials"
    code: int = status.HTTP_401_UNAUTHORIZED

    def __init__(self, msg: str):
        super().__init__(msg=msg, error=self.error, status_code=self.code)


class Custom400Exception(BaseHttpException):
    error: str = "bad_request"
    code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, msg: str, code: Optional[int] = None):
        super().__init__(msg=msg, error=self.error, status_code=code or self.code)
