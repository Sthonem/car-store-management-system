"""Configuration loaded from environment variables."""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./data/auth.db"

    # JWT
    jwt_secret_key: str = "change-me-in-production-this-is-development-only"
    jwt_algorithm: str = "HS256"
    jwt_expiry_minutes: int = 1440  # 24 hours

    # Service identity
    service_name: str = "auth_service"

    class Config:
        env_file = ".env"


settings = Settings()
