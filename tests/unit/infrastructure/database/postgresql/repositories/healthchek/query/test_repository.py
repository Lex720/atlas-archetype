from unittest.mock import patch

import pytest
from pytest_mock import MockerFixture

from src.infrastructure.database.postgresql.repositories.healthchek.query.repository import (  # noqa: E501
    Check as CheckRepository,
)


@pytest.mark.asyncio
class TestRepository:
    @patch(
        "src.infrastructure.database.postgresql.repositories.healthchek.query.repository.connect"  # noqa: E501
    )
    async def test_postgresql_repository_passed(
        self, connect_mock: MockerFixture
    ) -> None:
        check = CheckRepository()
        result = await check()

        assert not result

    async def test_postgresql_repository_not_passed(self) -> None:
        check = CheckRepository()

        with pytest.raises(OSError):
            await check()
