import sys

from fastapi.templating import Jinja2Templates
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    test: bool = Field("pytest" in sys.modules, validation_alias="TEST")
    DEBUG: bool = True

    BASE_URL: str = "http://localhost:8000"

    DB_NAME: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"

    DATABASE_POOL_SIZE: int = 5
    DATABASE_POOL_RECYCLE_SECONDS: int = 300

    templates: Jinja2Templates = Jinja2Templates(directory="api/templates")

    API_TOKEN: str

    templates: Jinja2Templates = Jinja2Templates(directory="api/templates")

    model_config = SettingsConfigDict(env_file="conf/.env", env_file_encoding="utf-8")

    @field_validator("DB_NAME", mode="before")
    def set_db_name(cls, db, info):
        if info.data["test"]:
            return "test_" + db
        return db

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
