from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from app.backend.api.services.action import ActionService
    from app.backend.api.services.classes import ClassesService
    from app.backend.api.services.external_user import ExternalUserService


class ServiceMediator:
    def __init__(self, session: AsyncSession):
        self.session = session

    @property
    def external_user(self) -> "ExternalUserService":
        from app.backend.api.services.external_user import ExternalUserService

        return ExternalUserService(session=self.session)

    @property
    def action(self) -> "ActionService":
        from app.backend.api.services.action import ActionService

        return ActionService(session=self.session)

    @property
    def classes(self) -> "ClassesService":
        from app.backend.api.services.classes import ClassesService

        return ClassesService(session=self.session)
