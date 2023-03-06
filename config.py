import os

from pydantic import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    POSTGRES_USER: str = Field(default="root")
    POSTGRES_PASSWORD: str = Field(default="root")
    POSTGRES_SERVER: str = Field(default="localhost")
    POSTGRES_PORT: str = Field(default="5432")
    POSTGRES_DB: str = Field(default="db")

    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: str = Field(default="6379")
    REDIS_SEP: str = Field(default=":")
    REDIS_PASSWORD: str = Field(default="root")
    REDIS_CREDS_DB: str = Field(default="0")
    REDIS_CLS_DB: str = Field(default="1")
    REDIS_GTP_DB: str = Field(default="2")

    SPREADSHEET_ID: str
    GOOGLE_SECRET: dict
    CHAT_GPT_TOKEN: str

    VK_DOMASHKA_TOKEN: str
    VK_RASPISANIE_TOKEN: str
    VK_KPKPKP_TOKEN: str
    VK_ADMIN_IDS: list[int]
    VK_EMPTY_MESSAGE: str = Field(default=".")

    PRODUCTION: bool = Field(default=False)
    NOT_EXISTING_GROUPS: list[int] = Field(default=[310, 127])

    class Config:
        env_file = os.getenv("ENV_LOC", ".env")
        env_file_encoding = "utf-8"

    @property
    def POSTGRES_URL(self):
        return "postgresql://{}:{}@{}/{}".format(
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_SERVER,
            self.POSTGRES_DB,
        )

    @property
    def POSTGRES_URL_ASYNC(self):
        return "postgresql+asyncpg://{}:{}@{}/{}".format(
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_SERVER,
            self.POSTGRES_DB,
        )

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/"


settings = Settings()
