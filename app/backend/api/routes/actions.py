from fastapi import APIRouter
from fastapi import Depends

from app.backend.api.dependencies.auth import get_current_user
from app.backend.api.routes.dto.action.request import ButtonActionPromptRequest
from app.backend.api.routes.dto.action.request import ButtonActionRequest
from app.backend.api.routes.dto.user.response import ExternalUser
from app.backend.api.services.action import ActionService
from app.backend.api.services.external_user import ExternalUserService
from app.backend.core.schemes import SuccessResponse
from app.backend.db.models.action import ButtonsEnum
from app.backend.db.models.user import ExternalUserModel
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


@actions_router.post(
    "/action/prompt",
    response_model=ExternalUser,
)
async def create_prompt_action(
    data: ButtonActionPromptRequest,
    service: ActionService = Depends(ActionService),
    user_service: ExternalUserService = Depends(ExternalUserService),
    current_user: UserModel = Depends(get_current_user),
) -> ExternalUserModel:
    await service.mark_action_button_clicked(
        button=ButtonsEnum.chat_gpt_prompt,
        pattern=data.pattern,
        user_id=data.user_id,
        current_user=current_user,
    )

    result = await user_service.get_user_by_external_id(
        telegram_id=data.telegram_id,
        vk_id=data.vk_id,
    )

    return result
