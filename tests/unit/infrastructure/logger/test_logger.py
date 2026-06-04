import pytest
from loguru import logger

from src.infrastructure.logger.config import configure_logging


@pytest.mark.asyncio
class TestConfig:
    async def test_configure_logging(self) -> None:
        configure_logging()
        result = logger.bind(tag="atlas_test_login").info("Configuring logger")

        assert not result
