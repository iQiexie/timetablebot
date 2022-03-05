from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    DB_URL: str = Field(default="sqlite+aiosqlite:///college.db")


settings = Settings()
