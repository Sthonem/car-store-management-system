"""Configuration from environment variables."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./data/catalog.db"

    # Where to call Auth Service. Inside Docker: http://auth_service:8001
    # Outside Docker (dev): http://localhost:8001
    auth_service_url: str = "http://auth_service:8001"

    service_name: str = "catalog_service"

    class Config:
        env_file = ".env"


settings = Settings()
