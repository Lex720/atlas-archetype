from unittest.mock import patch

import pytest
from pytest_mock import MockerFixture

from src.infrastructure.database.mongodb.repositories.healthchek.query.repository import (  # noqa: E501
    Check as CheckRepository,
)


@pytest.mark.asyncio
class TestRepository:
    @patch(
        "src.infrastructure.database.mongodb.repositories.healthchek.query.repository.connect"  # noqa: E501
    )
    async def test_mongodb_repository_passed(self, connect_mock: MockerFixture) -> None:
        check = CheckRepository()
        result = await check()

        assert not result

    @patch(
        "src.infrastructure.database.mongodb.repositories.healthchek.query.repository.connect",  # noqa: E501
        side_effect=OSError(),
    )
    async def test_mongodb_repository_not_passed(
        self, connect_mock: MockerFixture
    ) -> None:
        check = CheckRepository()

        with pytest.raises(OSError):
            await check()
