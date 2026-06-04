from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from pytest_mock import MockerFixture

from src.domain.game.command.entity import GameDefaults as GameDefaultsEntity
from src.infrastructure.database.mongodb.repositories.base import settings
from src.infrastructure.database.postgresql.repositories.base import (
    Base as BaseRepository,
)
from src.infrastructure.database.postgresql.repositories.game.command.repository import (  # noqa: E501
    Game as GameRepository,
)

uuid_mock = uuid4()
datetime_mock = datetime.now()
game_defaults_data_mock = {
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
game_defaults_entity_mock = GameDefaultsEntity(**game_defaults_data_mock)


@pytest.mark.asyncio
class TestRepository:
    @patch.object(BaseRepository, "_publish_to_broker")
    async def test_game_postgresql_repository_create_passed(
        self, _publish_to_broker_mock: MockerFixture
    ) -> None:
        settings.command_motor = "postgresql"
        session_mock = AsyncMock()
        repository = GameRepository(session_mock)
        result = await repository.create(
            game_defaults_entity_mock.model_dump(exclude_defaults=True)
        )

        assert result.get("uuid") == uuid_mock

    @patch.object(BaseRepository, "_publish_to_broker")
    async def test_game_postgresql_repository_create_not_passed(
        self, _publish_to_broker_mock: MockerFixture
    ) -> None:
        session_mock = AsyncMock()
        repository = GameRepository(session_mock)

        with pytest.raises(TypeError):
            await repository.create(None)

    @patch.object(BaseRepository, "_publish_to_broker")
    async def test_game_postgresql_repository_update_passed(
        self, _publish_to_broker_mock: MockerFixture
    ) -> None:
        settings.command_motor = "postgresql"
        session_mock = AsyncMock()
        result_mock = MagicMock()
        result_mock.first.return_value = game_defaults_entity_mock
        session_mock.scalars.return_value = result_mock
        repository = GameRepository(session_mock)
        result = await repository.update(
            uuid_mock, game_defaults_entity_mock.model_dump(exclude_defaults=True)
        )

        assert result.get("uuid") == uuid_mock

    @patch.object(BaseRepository, "_publish_to_broker")
    async def test_game_postgresql_repository_update_not_passed(
        self, _publish_to_broker_mock: MockerFixture
    ) -> None:
        session_mock = AsyncMock()
        repository = GameRepository(session_mock)

        with pytest.raises(TypeError):
            await repository.update(uuid_mock, None)

    @patch.object(BaseRepository, "_publish_to_broker")
    async def test_game_postgresql_repository_delete_passed(
        self, _publish_to_broker_mock: MockerFixture
    ) -> None:
        settings.command_motor = "postgresql"
        session_mock = AsyncMock()
        result_mock = MagicMock()
        result_mock.first.return_value = game_defaults_entity_mock
        session_mock.scalars.return_value = result_mock
        repository = GameRepository(session_mock)
        result = await repository.delete(uuid_mock)

        assert not result

    @patch.object(BaseRepository, "_publish_to_broker")
    async def test_game_postgresql_repository_delete_not_passed(
        self, _publish_to_broker_mock: MockerFixture
    ) -> None:
        session_mock = AsyncMock()
        session_mock.execute = None
        repository = GameRepository(session_mock)

        with pytest.raises(TypeError):
            await repository.delete(None)
