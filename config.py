import logging
from pydantic import BaseSettings, Field


def generate_db_url(user, password, host, port, db_name):
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"


def generate_redis_url(host, port):
    return f"redis://{host}:{port}/"


def generate_logging_level(level):
    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }
    return level_map.get(f'{level}')


class Settings(BaseSettings):
    class Config:
        env_file = '.env.stage'
        env_file_encoding = 'utf-8'

    DB_USER: str = Field(env="DB_USER")
    DB_PASSWORD: str = Field(env="DB_PASSWORD")
    DB_PORT: int = Field(env="DB_PORT")
    DB_HOST: str = Field(env="DB_HOST")
    DB_NAME: str = Field(env="DB_NAME")

    REDIS_HOST: str = Field(env="REDIS_HOST")
    REDIS_PORT: int = Field(env="REDIS_PORT")

    google_secret: dict = Field(env="GOOGLE_SECRET")
    spreadsheet_original_id: str = Field(env="SPREADSHEET_ID")
    spreadsheet_current_id: str = Field(default=None)  # TODO DELETE

    RASPISANIE_TOKEN: str = Field(env='RASPISANIE_TOKEN')
    DOMASHKA_TOKEN: str = Field(env='DOMASHKA_TOKEN')
    TEST_TOKEN: str = Field(env='TEST_TOKEN')
    MPGU_TOKEN: str = Field(env='MPGU_TOKEN')

    CLASSES_PER_DAY: int = Field(env='CLASSES_PER_DAY')
    LOGGING_LEVEL: str = Field(env='LOGGING_LEVEL')
    ADMIN_VK_IDS: list[int] = Field(env='ADMIN_VK_IDS')
    ACTUALIZER_TIMEOUT: int = Field(env='ACTUALIZER_TIMEOUT')
    PRODUCTION: bool = Field(env="PRODUCTION")

    @property
    def db_url(self):
        return generate_db_url(
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            db_name=self.DB_NAME
        )

    @property
    def redis_url(self):
        return generate_redis_url(host=self.REDIS_HOST, port=self.REDIS_PORT)

    @property
    def logging_level(self):
        return generate_logging_level(level=self.LOGGING_LEVEL)


settings = Settings()
