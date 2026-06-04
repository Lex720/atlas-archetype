import asyncio
import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="session")
class TestRoutes:
    @pytest.fixture(scope="class")
    def game_data_command_mock(self) -> dict:
        return {
            "name": "Test",
            "platform": "ps",
            "stock": 1,
            "price": 2,
            "active": "true",
            "condition": "new",
        }

    async def test_route_game_all(self, api_client: AsyncClient) -> None:
        response = await api_client.get("/game")

        assert response.status_code == status.HTTP_200_OK

    async def test_route_game_create(
        self,
        api_client: AsyncClient,
        game_data_command_mock: dict,
    ) -> None:
        response = await api_client.post("/game", json=game_data_command_mock)

        assert response.status_code == status.HTTP_201_CREATED

    async def test_route_game_update(
        self,
        api_client: AsyncClient,
        game_data_command_mock: dict,
    ) -> None:
        response = await api_client.post("/game", json=game_data_command_mock)
        response_content = response.json()
        response = await api_client.put(
            f"/game/{response_content.get('uuid')}",
            json=game_data_command_mock,
        )

        assert response.status_code == status.HTTP_201_CREATED

    async def test_route_game_delete(
        self,
        api_client: AsyncClient,
        game_data_command_mock: dict,
    ) -> None:
        response = await api_client.post("/game", json=game_data_command_mock)
        response_content = response.json()
        response = await api_client.delete(f"/game/{response_content.get('uuid')}")

        assert response.status_code == status.HTTP_200_OK

    async def test_route_game_get(
        self,
        api_client: AsyncClient,
        game_data_command_mock: dict,
    ) -> None:
        response = await api_client.post("/game", json=game_data_command_mock)
        response_content = response.json()
        await asyncio.sleep(5)
        response = await api_client.get(f"/game/{response_content.get('uuid')}")

        assert response.status_code == status.HTTP_200_OK
