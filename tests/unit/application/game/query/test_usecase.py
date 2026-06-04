from datetime import datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from pytest_mock import MockerFixture

from src.application.game.query.usecase import GameAll as GameAllUsecase
from src.application.game.query.usecase import GameGet as GameGetUsecase
from src.domain.game.exception import GameNotFoundError
from src.domain.game.query.entity import Game as GameEntity
from src.domain.game.query.entity import GameFilter as GameFilterEntity
from src.infrastructure.database.postgresql.repositories.game.query.repository import (
    Game as GameRepository,
)  # noqa: E501

session_mock = AsyncMock()
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
game_results_paginated_with_items = {
    "items": [game_data_mock, game_data_mock],
    "total": 2,
}
game_results_paginated_without_items = {
    "items": [],
    "total": 0,
}


@pytest.mark.asyncio
class TestUsecase:
    async def test_game_all_passed(self, mocker: MockerFixture) -> None:
        repository_mock = GameRepository(session_mock)
        mocker.patch.object(
            repository_mock, "all", return_value=game_results_paginated_with_items
        )
        usecase = GameAllUsecase(repository_mock)
        result = await usecase.execute(game_filter_entity_mock)

        assert result.get("total") == 2
        assert len(result.get("items")) == 2

    async def test_game_all_not_passed(self, mocker: MockerFixture) -> None:
        repository_mock = GameRepository(session_mock)
        mocker.patch.object(
            repository_mock, "all", return_value=game_results_paginated_without_items
        )
        usecase = GameAllUsecase(repository_mock)
        result = await usecase.execute(game_filter_entity_mock)

        assert result.get("total") == 0
        assert len(result.get("items")) == 0

    async def test_game_get_passed(self, mocker: MockerFixture) -> None:
        repository_mock = GameRepository(session_mock)
        mocker.patch.object(repository_mock, "get", return_value=game_data_mock)
        usecase = GameGetUsecase(repository_mock)
        result = await usecase.execute(uuid_mock)

        assert isinstance(result, GameEntity)
        assert result.active
        assert str(result.uuid) == uuid_mock
        assert result.name == game_data_mock.get("name")

    async def test_game_get_not_passed(self, mocker: MockerFixture) -> None:
        repository_mock = GameRepository(session_mock)
        mocker.patch.object(repository_mock, "get", return_value={})
        usecase = GameGetUsecase(repository_mock)

        with pytest.raises(GameNotFoundError):
            await usecase.execute(uuid_mock)
