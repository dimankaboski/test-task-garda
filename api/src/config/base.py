import os
from pydantic_settings import BaseSettings


class Base(BaseSettings):
    POSTGRES_DB_USER: str = os.getenv("POSTGRES_DB_USER")
    POSTGRES_DB_PASSWORD: str = os.getenv("POSTGRES_DB_PASSWORD")
    POSTGRES_DB_NAME: str = os.getenv("POSTGRES_DB_NAME")

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.POSTGRES_DB_USER}:{self.POSTGRES_DB_PASSWORD}@weather_postgres:5432/{self.POSTGRES_DB_NAME}"

    @property
    def DATABASE_URL_psycopg(self):
        return f"postgresql+psycopg://{self.POSTGRES_DB_USER}:{self.POSTGRES_DB_PASSWORD}@weather_postgres:5432/{self.POSTGRES_DB_NAME}"


base_config = Base()
