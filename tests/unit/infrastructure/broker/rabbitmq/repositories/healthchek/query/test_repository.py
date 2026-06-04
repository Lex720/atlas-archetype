import pytest
from pytest_mock import MockerFixture

from src.infrastructure.broker.rabbitmq.repositories.healthchek.query.repository import (  # noqa: E501
    Check as CheckRepository,
)


@pytest.mark.asyncio
class TestRepository:
    async def test_rabbitmq_repository_passed(self, mocker: MockerFixture) -> None:
        check = CheckRepository()
        mocker.patch(
            "src.infrastructure.broker.rabbitmq.repositories.healthchek.query.repository.connect_robust"  # noqa: E501
        )
        result = await check()

        assert result

    async def test_rabbitmq_repository_not_passed(self) -> None:
        check = CheckRepository()

        with pytest.raises(OSError):
            await check()
