from fastapi import APIRouter

from app.backend.api.routes.actions import actions_router
from app.backend.api.routes.auth import security_router
from app.backend.api.routes.classes import classes_router
from app.backend.api.routes.user import users_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(users_router, tags=["Юзеры"])
api_router.include_router(security_router, tags=["Авторизация"])
api_router.include_router(classes_router, tags=["Пары"])
api_router.include_router(actions_router, tags=["Телеметрия"])
