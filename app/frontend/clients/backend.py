import urllib.parse
from datetime import datetime
from functools import lru_cache

from app.backend.api.routes.dto.classes.request import DayRequest
from app.backend.api.routes.dto.classes.request import RateRequest
from app.backend.api.routes.dto.classes.response import ClassScheme
from app.backend.api.services.dto.classes import DURATIONS_MAP
from app.base_request_client import BaseRequestsClient
from app.frontend.dto.user import CreateUser
from app.frontend.dto.user import DaySchema
from app.frontend.dto.user import User
from config import settings


@lru_cache
class BackendApi(BaseRequestsClient):
    def __init__(self):
        self.base_url = settings.BACKEND_BASE_URL
        self.auth = {"Authorization": f"Bearer {settings.ADMIN_SECRET_KEY}"}
        self.raise_exceptions = True

    async def get_user(self, data: CreateUser) -> User:
        response = await self._make_request(
            method="POST",
            url="/v1/users/external",
            json=data.dict(),
        )

        return User(**response)

    async def update_user(self, data: CreateUser) -> User:
        response = await self._make_request(
            method="PATCH",
            url="/v1/users/external",
            json=data.dict(),
        )

        return User(**response)

    async def get_last_updated_at(self) -> datetime:
        response = await self._make_request(method="GET", url="/v1/classes/last_update")
        return response["last_update"]

    async def get_classes(self, data: DayRequest) -> DaySchema:
        params = data.dict(exclude_none=True)

        params = urllib.parse.urlencode(params)
        response = await self._make_request(
            method="GET",
            url=f"/v1/classes/days?{params}",
        )

        classes = [ClassScheme(**i) for i in response]

        day_schema = {DURATIONS_MAP[i.duration]: i for i in classes}

        return DaySchema(**day_schema)

    async def get_classes_pattern(self, data: DayRequest) -> DaySchema:
        params = data.dict(exclude_none=True)

        params = urllib.parse.urlencode(params)
        response = await self._make_request(
            method="GET",
            url=f"/v1/classes/pattern?{params}",
        )

        classes = [ClassScheme(**i) for i in response]

        day_schema = {DURATIONS_MAP[i.duration]: i for i in classes}

        return DaySchema(**day_schema)

    async def rate_class(self, data: RateRequest) -> None:
        data = data.json()
        url = "/v1/classes/rate"

        await self._make_request(method="POST", url=url, data=data)
