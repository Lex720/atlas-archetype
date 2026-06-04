from datetime import datetime
from uuid import UUID, uuid4

import pytest
from fastapi import status
from httpx import AsyncClient

from src.application.game.command.service import game_create as game_create_service
from src.application.game.command.service import game_delete as game_delete_service
from src.application.game.command.service import game_update as game_update_service
from src.application.game.query.service import game_all as game_all_service
from src.application.game.query.service import game_get as game_get_service
from src.presentation.api.main import api

uuid_mock = str(uuid4())
datetime_mock = datetime.now()
game_data_command_mock = {
    "name": "Test",
    "platform": "ps",
    "stock": 1,
    "price": 2,
    "active": "true",
    "condition": "new",
}
game_data_query_mock = game_data_command_mock.copy()
game_data_query_mock.update(
    {"uuid": uuid_mock, "created_at": datetime_mock, "updated_at": datetime_mock}
)


class GameAllUsecaseMock:
    async def execute(self, entity: dict) -> dict:
        return {"items": [], "total": 1, "page": 1, "size": 1, "pages": 1}


class GameGetUsecaseMock:
    async def execute(self, uuid: UUID) -> dict:
        return game_data_query_mock


class GameCreateUsecaseMock:
    async def execute(self, entity: dict) -> dict:
        return game_data_query_mock


class GameUpdateUsecaseMock:
    async def execute(self, uuid: UUID, entity: dict) -> dict:
        return game_data_query_mock


class GameDeleteUsecaseMock:
    async def execute(self, uuid: UUID) -> dict:
        return None


async def game_all_service_mock() -> GameAllUsecaseMock:
    return GameAllUsecaseMock()


async def game_get_service_mock() -> GameGetUsecaseMock:
    return GameGetUsecaseMock()


async def game_create_service_mock() -> GameCreateUsecaseMock:
    return GameCreateUsecaseMock()


async def game_update_service_mock() -> GameUpdateUsecaseMock:
    return GameUpdateUsecaseMock()


async def game_delete_service_mock() -> GameDeleteUsecaseMock:
    return GameDeleteUsecaseMock()


@pytest.mark.asyncio
class TestRoutes:
    async def test_route_game_all(self, api_client: AsyncClient) -> None:
        api.dependency_overrides[game_all_service] = game_all_service_mock
        response = await api_client.get("/game")

        assert response.status_code == status.HTTP_200_OK

    async def test_route_game_get(self, api_client: AsyncClient) -> None:
        api.dependency_overrides[game_get_service] = game_get_service_mock
        response = await api_client.get(f"/game/{uuid_mock}")

        assert response.status_code == status.HTTP_200_OK

    async def test_route_game_create(self, api_client: AsyncClient) -> None:
        api.dependency_overrides[game_create_service] = game_create_service_mock
        response = await api_client.post("/game", json=game_data_command_mock)

        assert response.status_code == status.HTTP_201_CREATED

    async def test_route_game_update(self, api_client: AsyncClient) -> None:
        api.dependency_overrides[game_update_service] = game_update_service_mock
        response = await api_client.put(
            f"/game/{uuid_mock}", json=game_data_command_mock
        )

        assert response.status_code == status.HTTP_201_CREATED

    async def test_route_game_delete(self, api_client: AsyncClient) -> None:
        api.dependency_overrides[game_delete_service] = game_delete_service_mock
        response = await api_client.delete(f"/game/{uuid_mock}")

        assert response.status_code == status.HTTP_200_OK
