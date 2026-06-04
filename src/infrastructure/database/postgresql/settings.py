from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings


class SettingsPostgresql(BaseSettings):
    """Postgresql dabatase settings needed for the application."""

    postgresql_url: str
    sqlalchemy_echo: bool | Literal["debug"] = False
    sqlalchemy_echo_pool: bool | Literal["debug"] = False
    sqlalchemy_pool_size: int = 5
    sqlalchemy_max_overflow_pool: int = 5
    sqlalchemy_pool_timeout: int = 30


@lru_cache
def get_settings_postgresql() -> SettingsPostgresql:
    """Returns instance for the settings class."""
    return SettingsPostgresql()
