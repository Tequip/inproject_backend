import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    APP_TITLE: str = "InProject"
    APP_VERSION: str = "v0.0.1"
    API_V1_STR: str = "/api"

    PG_DSN: str = os.getenv("PG_DSN")
    PG_CELERY_DSN: str = os.getenv("PG_CELERY_DSN")
    PG_ALEMBIC_DSN: str = os.getenv("PG_ALEMBIC_DSN")

    ALGORITHM: str = os.getenv("ALGORITHM")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_HOURS: int = os.getenv("REFRESH_TOKEN_EXPIRE_HOURS")

    OPEN_REGISTRATION: bool = os.getenv("OPEN_REGISTRATION")

    BROKER_URL: str = os.getenv("BROKER_URL")

    AUDIT: bool = os.getenv("AUDIT")

    COMMON_FILE_PATH: str = os.getenv("COMMON_FILE_PATH")

    DOMAIN: str = os.getenv("DOMAIN")
    RESOURCE_API: str = "/api/resource"

    class Config:
        case_sensitive = True


settings = Settings()
