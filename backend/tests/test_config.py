import pytest

from src.core.config import Settings, get_settings


def test_settings_requires_secret_key_with_minimum_length() -> None:
    with pytest.raises(ValueError, match="SECRET_KEY not set or too short"):
        Settings(SECRET_KEY="short")


def test_get_settings_returns_cached_settings_from_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("SECRET_KEY", "a" * 32)
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
    get_settings.cache_clear()

    settings = get_settings()

    assert settings.SECRET_KEY == "a" * 32
    assert settings.DATABASE_URL == "sqlite+aiosqlite:///./test.db"
    assert settings.DEBUG is True
    assert get_settings() is settings


def test_settings_defaults_without_env_file() -> None:
    settings = Settings(SECRET_KEY="b" * 32, DEBUG=False)

    assert settings.DEBUG is False
    assert settings.JWT_ALGORITHM == "HS256"
    assert settings.JWT_EXPIRATION_HOURS == 24
