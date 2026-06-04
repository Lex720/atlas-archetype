from unittest.mock import AsyncMock

import pytest

from src.application.game.query.service import game_all as game_all_service
from src.application.game.query.service import game_get as game_get_service
from src.application.game.query.usecase import GameAll as GameAllUseCase
from src.application.game.query.usecase import GameGet as GameGetUseCase


@pytest.mark.asyncio
class TestService:
    async def test_game_all_service(self) -> None:
        session_mock = AsyncMock()
        usecase = game_all_service(session_mock)

        assert isinstance(usecase, GameAllUseCase)

    async def test_game_get_service(self) -> None:
        session_mock = AsyncMock()
        usecase = game_get_service(session_mock)

        assert isinstance(usecase, GameGetUseCase)
