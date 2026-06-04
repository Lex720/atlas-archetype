from datetime import datetime
from uuid import uuid4

import pytest

from src.domain.game.query.entity import Game as GameEntity

uuid_mock = str(uuid4())
datetime_mock = datetime.now()
game_data_base_mock = {
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
game_data_fail_mock = game_data_base_mock.copy()
game_data_fail_mock.update({"stock": 0})


@pytest.mark.asyncio
class TestEntity:
    async def test_game_entity_passed(self) -> None:
        entity = GameEntity(**game_data_base_mock)

        assert isinstance(entity, GameEntity)

    async def test_game_entity_not_passed(self) -> None:
        with pytest.raises(ValueError):
            GameEntity(**game_data_fail_mock)
