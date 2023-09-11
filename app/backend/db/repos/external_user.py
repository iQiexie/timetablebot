from typing import Optional

from sqlalchemy import select

from app.backend.core.exceptions.decorators import expect_arguments
from app.backend.core.exceptions.decorators import expect_specific_arguments
from app.backend.core.repo import BaseRepo
from app.backend.db.models.user import ExternalUserModel


class ExternalUserRepo(BaseRepo[ExternalUserModel]):
    model = ExternalUserModel

    async def get_external_user_by_id(self, external_user_id: int) -> Optional[ExternalUserModel]:
        return await self.base_get_one(id=external_user_id)

    @expect_specific_arguments(arguments=("telegram_id", "vk_id"))
    async def update_external_user(
        self,
        telegram_id: Optional[int] = None,
        vk_id: Optional[int] = None,
        **kwargs,
    ) -> ExternalUserModel:
        if telegram_id:
            return await self.base_update(
                ExternalUserModel,
                ExternalUserModel.telegram_id == telegram_id,
                **kwargs,
            )
        elif vk_id:
            return await self.base_update(
                ExternalUserModel,
                ExternalUserModel.vk_id == vk_id,
                **kwargs,
            )

    @expect_specific_arguments(arguments=("telegram_id", "vk_id"))
    async def create_external_user(self, **kwargs) -> ExternalUserModel:
        model = ExternalUserModel(**kwargs)
        self.session.add(model)
        return model

    @expect_arguments
    async def get_user_by_external_id(
        self,
        telegram_id: Optional[int] = None,
        vk_id: Optional[int] = None,
    ) -> Optional[ExternalUserModel]:
        stmt = select(ExternalUserModel)

        if telegram_id:
            stmt = stmt.where(ExternalUserModel.telegram_id == telegram_id)
        else:
            stmt = stmt.where(ExternalUserModel.vk_id == vk_id)

        query = await self.session.execute(stmt)
        return query.scalar_one_or_none()
