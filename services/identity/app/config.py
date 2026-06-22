from functools import lru_cache
from pathlib import Path
from typing import Annotated, Literal

from fastapi import Depends
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

SERVICE_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SERVICE_DIR.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(SERVICE_DIR / ".env", REPO_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: Literal["development", "production"] = "development"
    secret_key: SecretStr
    algorithm: str = "HS256"
    database_url: str
    redis_url: str

    @property
    def jwt_secret(self) -> str:
        return self.secret_key.get_secret_value()


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

SettingsDep = Annotated[Settings, Depends(get_settings)]
