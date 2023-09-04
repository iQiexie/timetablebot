from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from app.backend.api.services import ExternalUserService
    from app.backend.api.services.classes import ClassesService
    from app.backend.db.repos.classes import ClassesRepo
    from app.backend.db.repos.credentials import CredentialsRepo
    from app.backend.api.services import ActionService


class ServiceMediator:
    def __init__(self, session: AsyncSession):
        self.session = session

    @property
    def external_user(self) -> "ExternalUserService":
        from app.backend.api.services import ExternalUserService

        return ExternalUserService(session=self.session)

    @property
    def action(self) -> "ActionService":
        from app.backend.api.services import ActionService

        return ActionService(session=self.session)

    @property
    def classes(self) -> "ClassesService":
        from app.backend.api.services.classes import ClassesService
        from app.backend.db.repos.classes import ClassesRepo
        from app.backend.db.repos.credentials import CredentialsRepo

        return ClassesService(
            classes_repo=ClassesRepo(session=self.session),
            credentials_repo=CredentialsRepo(session=self.session),
        )
