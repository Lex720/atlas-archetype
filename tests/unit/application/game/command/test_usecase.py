from datetime import datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from pytest_mock import MockerFixture

from src.application.game.command.usecase import GameCreate as GameCreateUsecase
from src.application.game.command.usecase import GameDelete as GameDeleteUsecase
from src.application.game.command.usecase import GameUpdate as GameUpdateUsecase
from src.domain.game.command.entity import Game as GameEntity
from src.domain.game.command.entity import GameDefaults as GameDefaultsEntity
from src.domain.game.exception import GameNotFoundError
from src.domain.game.query.entity import Game as GameEntityQuery
from src.infrastructure.database.postgresql.repositories.game.command.repository import (  # noqa: E501
    Game as GameRepository,
)

session_mock = AsyncMock()
uuid_mock = str(uuid4())
datetime_mock = datetime.now()
game_data_mock = {
    "name": "Test",
    "platform": "ps",
    "stock": 1,
    "price": 2,
    "active": True,
    "condition": "new",
}
game_entity_mock = GameEntity(**game_data_mock)
game_data_mock.update(
    {
        "uuid": uuid_mock,
        "created_at": datetime_mock,
        "updated_at": datetime_mock,
    }
)
game_defaults_entity_mock = GameDefaultsEntity(**game_data_mock)


@pytest.mark.asyncio
class TestUsecase:
    async def test_game_create_passed(self, mocker: MockerFixture) -> None:
        repository_mock = GameRepository(session_mock)
        mocker.patch.object(repository_mock, "create", return_value=game_data_mock)
        usecase = GameCreateUsecase(repository_mock)
        result = await usecase.execute(game_defaults_entity_mock)

        assert isinstance(result, GameEntityQuery)
        assert result.active
        assert str(result.uuid) == uuid_mock
        assert result.name == game_data_mock.get("name")

    async def test_game_create_not_passed(self, mocker: MockerFixture) -> None:
        repository_mock = GameRepository(session_mock)
        mocker.patch.object(repository_mock, "create", return_value={})
        usecase = GameCreateUsecase(repository_mock)

        with pytest.raises(GameNotFoundError):
            await usecase.execute(game_entity_mock)

    async def test_game_update_passed(self, mocker: MockerFixture) -> None:
        repository_mock = GameRepository(session_mock)
        mocker.patch.object(repository_mock, "update", return_value=game_data_mock)
        usecase = GameUpdateUsecase(repository_mock)
        result = await usecase.execute(uuid_mock, game_entity_mock)

        assert isinstance(result, GameEntityQuery)
        assert result.active
        assert str(result.uuid) == uuid_mock
        assert result.name == game_data_mock.get("name")

    async def test_game_update_not_passed(self, mocker: MockerFixture) -> None:
        repository_mock = GameRepository(session_mock)
        mocker.patch.object(repository_mock, "update", return_value={})
        usecase = GameUpdateUsecase(repository_mock)

        with pytest.raises(GameNotFoundError):
            await usecase.execute(uuid_mock, game_entity_mock)

    async def test_game_delete_passed(self, mocker: MockerFixture) -> None:
        repository_mock = GameRepository(session_mock)
        mocker.patch.object(repository_mock, "delete", return_value=True)
        usecase = GameDeleteUsecase(repository_mock)

        assert await usecase.execute(uuid_mock)
