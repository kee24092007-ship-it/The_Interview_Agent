"""Application configuration loaded from environment variables / .env file."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application settings.

    Values are read from environment variables or a .env file located in the
    backend directory (see .env.example for the template).
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "AI Interview Agent API"
    app_version: str = "0.1.0"
    debug: bool = True

    # Database
    database_url: str = "sqlite:///./interview_agent.db"

    # Security
    secret_key: str = "change-me-to-a-long-random-string"
    cors_origins: str = "http://localhost:3000"

    # AI provider (OpenAI-compatible)
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Return a cached singleton instance of the application settings."""
    return Settings()
