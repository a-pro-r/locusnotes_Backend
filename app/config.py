# app/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "LocusNotes API"

    # Environment settings
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "DEBUG"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()