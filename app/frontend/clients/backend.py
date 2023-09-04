from functools import lru_cache

from app.base_request_client import BaseRequestsClient
from app.frontend.dto.user import CreateUser
from app.frontend.dto.user import User
from config import settings


@lru_cache
class BackendApi(BaseRequestsClient):
    def __init__(self):
        self.base_url = settings.BACKEND_BASE_URL
        self.auth = {"Authorization": f"Bearer {settings.BACKEND_API_KEY}"}
        self.raise_exceptions = True

    async def get_user(self, data: CreateUser) -> User:
        response = await self._make_request(
            method="POST",
            url="/api/v1/users/external",
            json=data.dict(),
        )

        return User(**response)

    async def update_user(self, data: CreateUser) -> User:
        response = await self._make_request(
            method="PATCH",
            url="/api/v1/users/external",
            json=data.dict(),
        )

        return User(**response)
