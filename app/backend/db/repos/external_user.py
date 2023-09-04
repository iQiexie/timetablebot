from typing import Optional

from sqlalchemy import or_
from sqlalchemy import select

from app.backend.core.exceptions.decorators import expect_arguments
from app.backend.core.exceptions.decorators import expect_specific_arguments
from app.backend.core.repo import BaseRepo
from app.backend.db.models.user import ExternalUserModel


class ExternalUserRepo(BaseRepo[ExternalUserModel]):
    model = ExternalUserModel

    @expect_specific_arguments(arguments=("telegram_id", "vk_id"))
    async def update_external_user(
        self, telegram_id: Optional[int] = None, vk_id: Optional[int] = None, **kwargs
    ) -> ExternalUserModel:
        return await self.base_update(
            ExternalUserModel,
            or_(
                ExternalUserModel.telegram_id == telegram_id,
                ExternalUserModel.vk_id == vk_id,
            ),
            **kwargs,
        )

    @expect_specific_arguments(arguments=("telegram_id", "vk_id"))
    async def create_external_user(self, **kwargs) -> ExternalUserModel:
        model = ExternalUserModel(**kwargs)
        self.session.add(model)
        return model

    @expect_arguments
    async def get_user_by_external_id(
        self, telegram_id: Optional[int] = None, vk_id: Optional[int] = None
    ) -> Optional[ExternalUserModel]:
        stmt = select(ExternalUserModel).where(
            or_(
                ExternalUserModel.telegram_id == telegram_id,
                ExternalUserModel.vk_id == vk_id,
            )
        )

        query = await self.session.execute(stmt)
        return query.scalar_one_or_none()
