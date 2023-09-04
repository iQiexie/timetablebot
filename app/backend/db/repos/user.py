from datetime import datetime

from app.backend.core.repo import BaseRepo
from app.backend.db.models.action import UserActionModel
from app.backend.db.models.user import UserModel


class UserRepo(BaseRepo[UserModel]):
    model = UserModel

    async def create_user(self, **kwargs) -> UserModel:
        model = UserModel(**kwargs)
        self.session.add(model)
        return model

    async def create_action(self, **kwargs) -> UserActionModel:
        if not kwargs.get("created_at"):
            kwargs["created_at"] = datetime.now()

        model = UserActionModel(**kwargs)
        self.session.add(model)
        return model
