"""Settings module for the API Gateway using pydantic-settings."""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """API Gateway configuration loaded from environment variables."""

    # Application
    APP_NAME: str = "Banking AI-Agent Gateway"
    APP_VERSION: str = "1.0.0"

    # Intent Service (gRPC)
    INTENT_SERVICE_HOST: str = "localhost"
    INTENT_SERVICE_PORT: int = 50051

    # Ollama (Response Generation)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL_NAME: str = "gpt-oss:20b"
    OLLAMA_TIMEOUT: float = 120.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
