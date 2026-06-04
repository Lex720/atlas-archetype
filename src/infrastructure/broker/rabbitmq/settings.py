from functools import lru_cache

from pydantic_settings import BaseSettings


class SettingsRabbitmq(BaseSettings):
    """Rabbitmq broker settings needed for the application."""

    rabbitmq_host: str = "127.0.0.1"
    rabbitmq_port: int = 5672
    rabbitmq_user: str
    rabbitmq_password: str
    rabbitmq_vhost: str = "/"
    rabbitmq_prefetch_count: int = 100
    rabbitmq_queue_name: str = "atlas.service_bus.replicate"
    rabbitmq_delay_ms: int = 1000
    rabbitmq_max_retries: int = 3


@lru_cache
def get_settings_rabbitmq() -> SettingsRabbitmq:
    """Returns instance for the settings class."""
    return SettingsRabbitmq()
