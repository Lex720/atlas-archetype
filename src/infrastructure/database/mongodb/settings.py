from functools import lru_cache

from pydantic_settings import BaseSettings


class SettingsMongodb(BaseSettings):
    """Mongodb database settings needed for the application."""

    mongodb_url: str
    mongodb_database: str


@lru_cache
def get_settings_mongodb() -> SettingsMongodb:
    """Returns instance for the settings class."""
    return SettingsMongodb()
