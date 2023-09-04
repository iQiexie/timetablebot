from app.backend.core.repo import BaseRepo
from app.backend.db.models.user import UserActionModel
from app.backend.db.models.user import UserModel


class UserRepo(BaseRepo[UserModel]):
    model = UserModel

    async def create_user(self, **kwargs) -> UserModel:
        model = UserModel(**kwargs)
        self.session.add(model)
        return model

    async def create_action(self, **kwargs) -> UserActionModel:
        model = UserActionModel(**kwargs)
        self.session.add(model)
        return model
