from datetime import datetime
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest
from pytest_mock import MockerFixture
from beanie.exceptions import CollectionWasNotInitialized

from src.domain.game.command.entity import GameDefaults as GameDefaultsEntity
from src.infrastructure.database.mongodb.repositories.base import settings
from src.infrastructure.database.mongodb.repositories.game.command.repository import (
    Game as GameRepository,
)


class GameDefaultsEntityFake(GameDefaultsEntity):
    async def update(self, data: dict) -> bool:
        return True

    async def delete(self) -> bool:
        return True


uuid_mock = str(uuid4())
datetime_mock = datetime.now()
game_defaults_data_mock = {
    "_id": uuid_mock,
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
game_defaults_entity_mock = GameDefaultsEntityFake(**game_defaults_data_mock)


class GameModelMock:
    def __init__(self) -> None:
        self.uuid = uuid_mock

    def __call__(self, *args, **kwargs) -> None:
        return self

    async def find_one(self, filter: dict) -> dict:
        return game_defaults_entity_mock

    async def insert(self) -> dict:
        return game_defaults_entity_mock

    def model_dump(self) -> dict:
        return game_defaults_data_mock


@pytest.mark.asyncio
class TestRepository:
    @patch.object(GameRepository, "_publish_to_broker")
    @patch(
        "src.infrastructure.database.mongodb.repositories.game.command.repository.GameModel",  # noqa: E501
        wraps=GameModelMock(),
    )
    async def test_game_mongodb_repository_create_passed(
        self,
        _publish_to_broker_mock: MockerFixture,
        game_model_mock: MockerFixture,
    ) -> None:
        settings.command_motor = "mongodb"
        session_mock = AsyncMock()
        repository = GameRepository(session_mock)
        result = await repository.create(
            game_defaults_entity_mock.model_dump(exclude_defaults=True)
        )

        assert result.get("uuid") == uuid_mock

    @patch.object(GameRepository, "_publish_to_broker")
    async def test_game_mongodb_repository_create_not_passed(
        self,
        _publish_to_broker_mock: MockerFixture,
    ) -> None:
        repository = GameRepository(None)

        with pytest.raises(CollectionWasNotInitialized):
            await repository.create(
                game_defaults_entity_mock.model_dump(exclude_defaults=True)
            )

    @patch.object(GameRepository, "_publish_to_broker")
    @patch(
        "src.infrastructure.database.mongodb.repositories.game.command.repository.GameModel",  # noqa: E501
        wraps=GameModelMock(),
    )
    async def test_game_mongodb_repository_update_passed(
        self, _publish_to_broker_mock: MockerFixture, game_model_mock: MockerFixture
    ) -> None:
        settings.command_motor = "mongodb"
        session_mock = AsyncMock()
        repository = GameRepository(session_mock)
        result = await repository.update(
            uuid_mock, game_defaults_entity_mock.model_dump(exclude_defaults=True)
        )

        assert result.get("uuid") == uuid_mock

    @patch.object(GameRepository, "_publish_to_broker")
    async def test_game_mongodb_repository_update_not_passed(
        self, _publish_to_broker_mock: MockerFixture
    ) -> None:
        repository = GameRepository(None)

        with pytest.raises(AttributeError):
            await repository.update(
                uuid_mock, game_defaults_entity_mock.model_dump(exclude_defaults=True)
            )

    @patch.object(GameRepository, "_publish_to_broker")
    @patch(
        "src.infrastructure.database.mongodb.repositories.game.command.repository.GameModel",  # noqa: E501
        wraps=GameModelMock(),
    )
    async def test_game_mongodb_repository_delete_passed(
        self, _publish_to_broker_mock: MockerFixture, game_model_mock: MockerFixture
    ) -> None:
        settings.command_motor = "mongodb"
        session_mock = AsyncMock()
        repository = GameRepository(session_mock)
        result = await repository.delete(uuid_mock)

        assert not result

    @patch.object(GameRepository, "_publish_to_broker")
    async def test_game_mongodb_repository_delete_not_passed(
        self, _publish_to_broker_mock: MockerFixture
    ) -> None:
        repository = GameRepository(None)

        with pytest.raises(AttributeError):
            await repository.delete(uuid_mock)
