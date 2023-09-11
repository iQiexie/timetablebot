from fastapi import APIRouter
from fastapi import Depends

from app.backend.api.dependencies.auth import get_current_user
from app.backend.api.routes.dto.action.request import ButtonActionRequest
from app.backend.api.services.action import ActionService
from app.backend.core.schemes import SuccessResponse
from app.backend.db.models.user import UserModel

actions_router = APIRouter()


@actions_router.post(
    "/action/button",
    response_model=SuccessResponse,
)
async def create_action(
    data: ButtonActionRequest,
    service: ActionService = Depends(ActionService),
    current_user: UserModel = Depends(get_current_user),
) -> SuccessResponse:
    await service.mark_action_button_clicked(
        **data.dict(),
        current_user=current_user,
    )
    return SuccessResponse(success=True)
