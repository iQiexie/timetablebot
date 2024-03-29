from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.backend.api.routes.dto.auth.request import TokenModel
from app.backend.api.services.auth import SecurityService
from app.backend.db.repos.user import UserRepo
from config import settings

security_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.BACKEND_BASE_URL_SWAGGER}/v1/security/token",
)


@security_router.post("/security/token", response_model=TokenModel)
async def get_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    users: UserRepo = Depends(UserRepo),
) -> TokenModel:
    return await SecurityService().authenticate(
        password=form_data.password,
        username=form_data.username,
        users=users,
    )
