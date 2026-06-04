from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings

ALLOWED_MOTORS = {"postgresql", "mongodb"}


class SettingsGlobal(BaseSettings):
    """Global settings needed for the application."""

    query_motor: str = ""
    command_motor: str = ""

    cors_origins: list[str] = ["http://localhost", "http://localhost:8080"]
    cors_allow_credentials: bool = False
    cors_allow_methods: list[str] = ["GET", "POST", "PUT", "DELETE"]
    cors_allow_headers: list[str] = ["Content-Type", "Authorization"]

    @field_validator("command_motor", "query_motor")
    @classmethod
    def validate_motor(cls, value: str) -> str:
        """Validate motor is in the allowed set."""
        if value and value not in ALLOWED_MOTORS:
            raise ValueError(f"Invalid motor '{value}'. Allowed: {ALLOWED_MOTORS}")
        return value


@lru_cache
def get_settings_global() -> SettingsGlobal:
    """Returns instance for the settings class."""
    return SettingsGlobal()
