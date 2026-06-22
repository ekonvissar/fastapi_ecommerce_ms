from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    identity_url: str = "http://identity:8000"
    catalog_url: str = "http://catalog:8000"
    ordering_url: str = "http://ordering:8000"

    auth_cookie_path: str = "/api/v1/auth"


@lru_cache
def get_settings() -> Settings:
    return Settings()
