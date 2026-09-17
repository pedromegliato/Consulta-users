from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env", extra="ignore")

    provider_base_url: str = "https://jsonplaceholder.typicode.com"
    provider_timeout_seconds: float = 5.0

    max_concurrency: int = 10
    retry_attempts: int = 3
    retry_base_delay_seconds: float = 0.2
    retry_max_delay_seconds: float = 2.0

    cache_ttl_seconds: int = 60
    redis_url: str | None = None
    database_url: str | None = None

    cors_origins: list[str] = ["http://localhost:5173"]
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
