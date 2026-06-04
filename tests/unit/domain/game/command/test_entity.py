from datetime import datetime
from uuid import uuid4

import pytest

from src.domain.game.command.entity import Game as GameEntity
from src.domain.game.command.entity import GameDefaults as GameDefaultsEntity

uuid_mock = str(uuid4())
datetime_mock = datetime.now()
game_data_base_mock = {
    "name": "Test",
    "platform": "ps",
    "stock": 1,
    "price": 2,
    "active": True,
    "condition": "new",
    "updated_at": datetime_mock,
}
game_data_fail_mock = game_data_base_mock.copy()
game_data_fail_mock.update({"condition": "defective"})
game_data_defaults_mock = game_data_base_mock.copy()
game_data_defaults_mock.update(
    {
        "uuid": uuid_mock,
        "created_at": datetime_mock,
    }
)
game_data_defaults_fail_mock = game_data_base_mock.copy()
game_data_defaults_fail_mock.update({"stock": 0})


@pytest.mark.asyncio
class TestEntity:
    async def test_game_entity_passed(self) -> None:
        entity = GameEntity(**game_data_base_mock)

        assert isinstance(entity, GameEntity)

    async def test_game_entity_not_passed(self) -> None:
        with pytest.raises(ValueError):
            GameEntity(**game_data_fail_mock)

    async def test_game_defaults_entity_passed(self) -> None:
        entity = GameDefaultsEntity(**game_data_defaults_mock)

        assert isinstance(entity, GameDefaultsEntity)

    async def test_game_defaults_entity_not_passed(self) -> None:
        with pytest.raises(ValueError):
            GameDefaultsEntity(**game_data_defaults_fail_mock)
