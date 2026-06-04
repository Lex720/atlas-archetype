from unittest.mock import AsyncMock

import pytest

from src.application.game.command.service import game_create as game_create_service
from src.application.game.command.service import game_delete as game_delete_service
from src.application.game.command.service import game_update as game_update_service
from src.application.game.command.usecase import GameCreate as GameCreateUseCase
from src.application.game.command.usecase import GameDelete as GameDeleteUseCase
from src.application.game.command.usecase import GameUpdate as GameUpdateUseCase


@pytest.mark.asyncio
class TestService:
    async def test_game_create_service(self) -> None:
        session_mock = AsyncMock()
        usecase = game_create_service(session_mock)

        assert isinstance(usecase, GameCreateUseCase)

    async def test_game_update_service(self) -> None:
        session_mock = AsyncMock()
        usecase = game_update_service(session_mock)

        assert isinstance(usecase, GameUpdateUseCase)

    async def test_game_delete_service(self) -> None:
        session_mock = AsyncMock()
        usecase = game_delete_service(session_mock)

        assert isinstance(usecase, GameDeleteUseCase)
