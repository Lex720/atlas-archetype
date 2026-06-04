from datetime import datetime
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest
from motor.motor_asyncio import AsyncIOMotorCollection
from pytest_mock import MockerFixture

from src.domain.game.query.entity import Game as GameEntity
from src.domain.game.query.entity import GameFilter as GameFilterEntity
from src.infrastructure.database.mongodb.repositories.game.query.repository import (
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


async def get_paginated_instances_mock(
    collection: AsyncIOMotorCollection, query_filter: dict, sort: dict
) -> dict:
    return paginated_instances_mock


class GameModelMock:
    def __init__(self) -> None:
        self.uuid = uuid_mock

    async def find_one(self, filter: dict) -> dict:
        return game_entity_mock


@pytest.mark.asyncio
class TestRepository:
    @patch(
        "src.infrastructure.database.mongodb.repositories.game.query.repository.paginate",  # noqa: E501
        wraps=get_paginated_instances_mock,
    )
    @patch.object(GameRepository, "collection")
    async def test_game_mongodb_repository_all_passed(
        self,
        paginate_mock: MockerFixture,
        collection_mock: MockerFixture,
    ) -> None:
        session_mock = AsyncMock()
        repository = GameRepository(session_mock)
        result = await repository.all(
            game_filter_entity_mock.model_dump(exclude_none=True)
        )

        assert len(result) == 1

    @patch(
        "src.infrastructure.database.mongodb.repositories.game.query.repository.paginate",  # noqa: E501
        side_effect=AttributeError(),
    )
    async def test_game_mongodb_repository_all_not_passed(
        self, paginate_mock: MockerFixture
    ) -> None:
        session_mock = AsyncMock()
        repository = GameRepository(session_mock)

        with pytest.raises(AttributeError):
            await repository.all(game_filter_entity_mock.model_dump(exclude_none=True))

    @patch(
        "src.infrastructure.database.mongodb.repositories.game.query.repository.GameModel",  # noqa: E501
        wraps=GameModelMock(),
    )
    async def test_game_mongodb_repository_get_passed(
        self,
        game_model_mock: MockerFixture,
    ) -> None:
        session_mock = AsyncMock()
        repository = GameRepository(session_mock)
        result = await repository.get(uuid_mock)

        assert str(result.get("uuid")) == uuid_mock

    async def test_game_mongodb_repository_get_not_passed(self) -> None:
        repository = GameRepository(None)

        with pytest.raises(AttributeError):
            await repository.get(uuid_mock)
