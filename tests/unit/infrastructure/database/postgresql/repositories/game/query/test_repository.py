from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from pytest_mock import MockerFixture

from src.domain.game.query.entity import Game as GameEntity
from src.domain.game.query.entity import GameFilter as GameFilterEntity
from src.infrastructure.database.postgresql.repositories.game.query.repository import (
    Game as GameRepository,
)

uuid_mock = str(uuid4())
datetime_mock = datetime.now()
game_data_mock = {
    "uuid": uuid_mock,
    "name": "Test",
    "platform": "ps",
    "stock": 1,
    "price": 2,
    "active": True,
    "condition": "new",
    "created_at": datetime_mock,
    "updated_at": datetime_mock,
}
game_entity_mock = GameEntity(**game_data_mock)
game_filter_data_mock = {"platform": None}
game_filter_entity_mock = GameFilterEntity(**game_filter_data_mock)
paginated_instances_mock = {"items": [game_entity_mock]}


async def get_paginated_instances_mock(session: AsyncMock, query: dict) -> dict:
    return paginated_instances_mock


@pytest.mark.asyncio
class TestRepository:
    @patch(
        "src.infrastructure.database.postgresql.repositories.base.paginate",
        wraps=get_paginated_instances_mock,
    )
    async def test_game_postgresql_repository_all_passed(
        self, paginate_mock: MockerFixture
    ) -> None:
        session_mock = AsyncMock()
        repository = GameRepository(session_mock)
        result = await repository.all(
            game_filter_entity_mock.model_dump(exclude_none=True)
        )

        assert len(result) == 1

    @patch(
        "src.infrastructure.database.postgresql.repositories.base.paginate",
        side_effect=AttributeError(),
    )
    async def test_game_postgresql_repository_all_not_passed(
        self, paginate_mock: MockerFixture
    ) -> None:
        session_mock = AsyncMock()
        repository = GameRepository(session_mock)

        with pytest.raises(AttributeError):
            await repository.all(game_filter_entity_mock.model_dump(exclude_none=True))

    async def test_game_postgresql_repository_get_passed(self) -> None:
        session_mock = AsyncMock()
        result_mock = MagicMock()
        result_mock.first.return_value = game_entity_mock
        session_mock.scalars.return_value = result_mock

        repository = GameRepository(session_mock)
        result = await repository.get(uuid_mock)

        assert str(result.get("uuid")) == uuid_mock

    async def test_game_postgresql_repository_get_not_passed(self) -> None:
        session_mock = AsyncMock()
        session_mock.scalars.return_value = None
        repository = GameRepository(session_mock)

        with pytest.raises(AttributeError):
            await repository.get(uuid_mock)
