import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.backend.api.dispatcher import api_router
from app.backend.core.exceptions.middlewares import ExceptionMiddleware
from config import settings


def init_logger() -> None:
    logging.basicConfig(level=logging.DEBUG)

    logger = logging.getLogger().handlers[0]
    log_format = "%(asctime)-15s | %(levelname).1s | %(name)8s |  %(message)s"
    logger.setFormatter(logging.Formatter(log_format))


def get_app() -> FastAPI:
    init_logger()

    fastapi_app = FastAPI(
        title=settings.APP_TITLE,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        swagger_ui_parameters={
            "displayRequestDuration": True,
            "filter": True,
        },
    )

    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    fastapi_app.add_middleware(ExceptionMiddleware)
    fastapi_app.include_router(api_router)

    return fastapi_app


app = get_app()
