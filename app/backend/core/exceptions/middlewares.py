from traceback import print_exception
from typing import Any, Callable

from fastapi import Request
from fastapi.exceptions import ResponseValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.backend.core.exceptions.http_exceptions import HTTPExceptionDetail


def handle_exception(exception: Exception, message: Any) -> JSONResponse:
    detail = {"type": str(type(exception)), "message": message}
    print_exception(exception)
    detail = HTTPExceptionDetail(
        error="internal_server_error",
        detail=detail,
        msg="Internal Server Error Occurred",
    )
    return JSONResponse(status_code=500, content=detail.dict())


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Any:
        try:
            return await call_next(request)
        except ResponseValidationError as e:
            return handle_exception(exception=e, message=str(e.errors()))
        except Exception as e:
            return handle_exception(exception=e, message=str(e))


class EmptyArgumentsError(RuntimeError):
    def __init__(self, arguments: list[str]):
        msg = f"Provide at least one argument of {arguments}"
        super().__init__(msg)
