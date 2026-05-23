"""Settings module for Intent Service using pydantic-settings."""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Intent Service configuration loaded from environment variables."""

    OLLAMA_BASE_URL: str = "http://localhost:11434"
    INTENT_MODEL_NAME: str = "gpt-oss:20b"
    GRPC_PORT: int = 50051

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
