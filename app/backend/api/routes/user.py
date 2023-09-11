from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from app.backend.api.dependencies.auth import get_current_user
from app.backend.api.routes.dto.user.request import ExternalUserCreate
from app.backend.api.routes.dto.user.request import ExternalUserUpdate
from app.backend.api.routes.dto.user.request import UserIn
from app.backend.api.routes.dto.user.response import ExternalUser
from app.backend.api.routes.dto.user.response import UserOut
from app.backend.api.services.external_user import ExternalUserService
from app.backend.api.services.user import UserService
from app.backend.db.models.user import UserModel

users_router = APIRouter()


@users_router.post("/users", response_model=UserOut)
async def create_user(
    user: UserIn,
    service: UserService = Depends(UserService),
    _: UserModel = Depends(get_current_user),
) -> UserModel:
    return await service.create_user(data=user)


@users_router.get("/users", response_model=UserOut)
async def get_user(
    user_id: int = Query(default=None),
    user_name: str = Query(default=None),
    service: UserService = Depends(UserService),
    _: UserModel = Depends(get_current_user),
) -> Optional[UserModel]:
    return await service.get_user(user_id=user_id, user_name=user_name)


@users_router.patch(
    path="/users/external",
    response_model=ExternalUser,
)
async def update_group_number(
    data: ExternalUserUpdate,
    service: ExternalUserService = Depends(ExternalUserService),
    current_user: UserModel = Depends(get_current_user),
) -> ExternalUser:
    return await service.update_external_user(
        data=data,
        current_user=current_user,
    )


@users_router.post(
    path="/users/external",
    response_model=ExternalUser,
)
async def get_or_create_external_user(
    data: ExternalUserCreate,
    service: ExternalUserService = Depends(ExternalUserService),
    _: UserModel = Depends(get_current_user),
) -> ExternalUserCreate:
    return await service.create_external_user(data=data)
