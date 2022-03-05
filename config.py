from typing import Optional

from pydantic import BaseSettings, Field


def generate_db_url(user, password, host, port, db_name):
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"


class Settings(BaseSettings):
    DB_USER: str = Field(env="DB_USER")
    DB_PASSWORD: str = Field(env="DB_PASSWORD")
    DB_PORT: int = Field(env="DB_PORT")
    DB_HOST: str = Field(env="DB_HOST")
    DB_NAME: str = Field(env="DB_NAME")

    google_secret: dict = Field(env="GOOGLE_SECRET")
    spreadsheet_current: Optional[str] = Field(default=None)

    @property
    def db_url(self):
        return generate_db_url(
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            db_name=self.DB_NAME
        )

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
