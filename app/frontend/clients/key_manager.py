from datetime import datetime
from typing import List
from typing import Optional

from pydantic import BaseModel

from app.singleton import MetaSingleton
from config import settings


class ApiKey(BaseModel):
    key: str
    available_after: datetime
    terminated: bool


class ApiKeyList(BaseModel):
    available_keys: int
    keys: List[ApiKey]


class ApiKeysManager(metaclass=MetaSingleton):
    initialized: bool
    keys: List[ApiKey]

    def __init__(self):
        self.initialized = True
        self.keys = [
            ApiKey(
                key=key,
                available_after=datetime.now(),
                terminated=False,
            )
            for key in settings.GPT_PROVIDER_KEYS
        ]

    @staticmethod
    def _key_valid(key: ApiKey) -> bool:
        return key.terminated is False and key.available_after < datetime.now()

    def get_key(self) -> Optional[str]:
        for key in self.keys:
            if self._key_valid(key):
                return key.key

    def terminate_key(self, key: str) -> str:
        for index, value in enumerate(self.keys):
            if value.key == key:
                value.terminated = True
                self.keys[index] = value
                return value.key

    def freeze_key(self, key: str, available_after: datetime) -> bool:
        for index, value in enumerate(self.keys):
            if value.key == key:
                value.available_after = available_after
                self.keys[index] = value
                return True

    def keys_count(self) -> int:
        return len(self.keys)

    def get_keys(self) -> str:
        available_keys = 0

        for key in self.keys:
            if self._key_valid(key):
                available_keys += 1

        return ApiKeyList(
            keys=self.keys,
            available_keys=available_keys,
        ).json()


gpt_keys_manager = ApiKeysManager()
