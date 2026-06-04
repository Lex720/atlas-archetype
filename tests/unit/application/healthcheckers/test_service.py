import pytest

from src.application.healthcheckers.service import (
    mongodb_check as mongodb_check_service,
)
from src.application.healthcheckers.service import (
    postgresql_check as postgresql_check_service,
)
from src.application.healthcheckers.service import (
    rabbitmq_check as rabbitmq_check_service,
)
from src.application.healthcheckers.usecase import Check


@pytest.mark.asyncio
class TestService:
    async def test_postgresql_check_service(self) -> None:
        usecase = postgresql_check_service()

        assert isinstance(usecase, Check)

    async def test_mongodb_check_service(self) -> None:
        usecase = mongodb_check_service()

        assert isinstance(usecase, Check)

    async def test_rabbitmq_check_service(self) -> None:
        usecase = rabbitmq_check_service()

        assert isinstance(usecase, Check)
