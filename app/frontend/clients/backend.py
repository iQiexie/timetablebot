import json
import urllib.parse
from datetime import datetime
from functools import lru_cache
from typing import Optional

from app.backend.api.routes.dto.classes.request import RateRequest
from app.backend.api.routes.dto.classes.response import ClassScheme
from app.backend.api.services.dto.classes import DURATIONS_MAP
from app.base_request_client import BaseRequestsClient
from app.frontend.common.dto.user import CreateUser
from app.frontend.common.dto.user import DayRequest
from app.frontend.common.dto.user import DaySchema
from app.frontend.common.dto.user import User
from config import settings


@lru_cache
class BackendApi(BaseRequestsClient):
    def __init__(self, token: str):
        self.base_url = settings.BACKEND_BASE_URL
        self.auth = {"Authorization": f"Bearer {token}"}
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

    async def get_last_updated_at(self) -> str:
        response = await self._make_request(method="GET", url="/v1/classes/last_update")
        uptime = response["last_update"]
        date_obj = datetime.fromisoformat(uptime)
        classes_uptime = date_obj.strftime("%H:%M, %d.%m.%Y")
        return classes_uptime

    async def get_classes(self, data: DayRequest, is_webapp: bool) -> DaySchema:
        params = data.dict(exclude_none=True)
        params["is_webapp"] = is_webapp

        params = urllib.parse.urlencode(params)
        response = await self._make_request(
            method="GET",
            url=f"/v1/classes/days?{params}",
        )

        classes = [ClassScheme(**i) for i in response]
        day_schema = {DURATIONS_MAP[i.duration]: i for i in classes}

        return DaySchema(**day_schema)

    async def get_classes_pattern(self, data: DayRequest, is_webapp: bool) -> DaySchema:
        params = data.dict(exclude_none=True)
        params["is_webapp"] = is_webapp

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

    async def mark_action(
        self,
        button_name: str,
        user_id: int,
        pattern: Optional[str] = None,
    ) -> None:
        data = json.dumps(
            {
                "button": button_name,
                "user_id": user_id,
                "pattern": pattern,
            }
        )
        url = "/v1/action/button"

        await self._make_request(method="POST", url=url, data=data)

    async def mark_prompt(
        self,
        user_id: int,
        pattern: str,
        vk_id: Optional[int] = None,
        telegram_id: Optional[int] = None,
    ) -> User:
        url = "/v1/action/prompt"
        data = json.dumps(
            {"user_id": user_id, "vk_id": vk_id, "telegram_id": telegram_id, "pattern": pattern}
        )

        response = await self._make_request(method="POST", url=url, data=data)
        return User(**response)
