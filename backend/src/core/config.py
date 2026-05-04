from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration from environment variables."""

    SECRET_KEY: str = ""
    DATABASE_URL: str = "sqlite+aiosqlite:///./jetson_facelock.db"
    DEBUG: bool = False
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    @model_validator(mode="after")
    def validate_secret_key(self) -> "Settings":
        if not self.SECRET_KEY or len(self.SECRET_KEY) < 32:
            raise ValueError(
                "SECRET_KEY not set or too short (min 32 characters). "
                'Run: python3 -c "import secrets; print(secrets.token_hex(32))" '
                "and set in .env"
            )
        return self


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance for dependency injection."""

    return Settings()
