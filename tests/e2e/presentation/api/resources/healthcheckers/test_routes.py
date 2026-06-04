import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.presentation.api.resources.healthcheckers.dtos import (
    LivezResponse as LivezResponseDTO,
)


@pytest.mark.asyncio(loop_scope="session")
class TestHealthCheckersRoutes:
    async def test_livez_ok(self, api_client: TestClient) -> None:
        response = await api_client.get("/healthchecks/livez")
        response_content = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_content["error"] is False
        assert response_content["message"] == "Successful call to livez"
        assert response_content["data"] == LivezResponseDTO().model_dump()

    async def test_readyz_ok(self, api_client: TestClient) -> None:
        response = await api_client.get("/healthchecks/readyz")
        response_content = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_content["error"] is False
        assert response_content["message"] == "Successful call to readyz"
