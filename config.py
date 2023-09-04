import os
from enum import Enum

from pydantic import BaseSettings
from pydantic import Field


class TimeMeasurementUnits(str, Enum):
    days = "days"
    seconds = "seconds"
    microseconds = "microseconds"
    milliseconds = "milliseconds"
    minutes = "minutes"
    hours = "hours"
    weeks = "weeks"


class Settings(BaseSettings):
    APP_TITLE: str
    BACKEND_CORS_ORIGINS: list[str] = Field(default=["*"])
    ADMIN_SECRET_KEY: str

    BACKEND_BASE_URL: str
    BACKEND_BASE_URL_SWAGGER: str

    JWT_SECRET: str
    SECRET_EXPIRATION_TIME: int
    SECRET_MEASUREMENT_UNIT: TimeMeasurementUnits

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    VK_TOKEN: str
    VK_ADMIN_IDS: list[str]
    VK_EMPTY_MESSAGE: str

    SPREADSHEET_ID: str
    GOOGLE_SECRET: dict

    @property
    def POSTGRES_URL(self) -> str:  # noqa
        return "postgresql://{}:{}@{}/{}".format(
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_SERVER,
            self.POSTGRES_DB,
        )

    @property
    def POSTGRES_URL_ASYNC(self) -> str:  # noqa
        return "postgresql+asyncpg://{}:{}@{}/{}".format(
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_SERVER,
            self.POSTGRES_DB,
        )

    class Config:
        env_file = os.getenv("ENV_FILE", ".env")
        env_file_encoding = "utf-8"


settings = Settings()
