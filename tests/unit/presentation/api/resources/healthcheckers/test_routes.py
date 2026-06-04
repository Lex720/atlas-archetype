from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import status
from httpx import ASGITransport, AsyncClient

from src.application.healthcheckers.service import health_check as health_check_service
from src.application.healthcheckers.usecase import HealthCheck as HealthCheckUseCase
from src.presentation.api.main import api
from src.presentation.api.resources.healthcheckers.dtos import (
    LivezResponse as LivezResponseDTO,
)


async def get_health_check_mock() -> HealthCheckUseCase:
    return HealthCheckUseCase([])


api.dependency_overrides[health_check_service] = get_health_check_mock


@pytest.mark.asyncio
class TestRoutes:
    @pytest_asyncio.fixture(scope="class")
    async def api_client(self) -> AsyncGenerator[AsyncClient, None]:
        transport = ASGITransport(app=api, raise_app_exceptions=False)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client

    async def test_route_healthcheckers_livez(self, api_client: AsyncClient) -> None:
        response = await api_client.get("/healthchecks/livez")
        response_content = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_content["error"] is False
        assert response_content["message"] == "Successful call to livez"
        assert response_content["data"] == LivezResponseDTO().model_dump()

    async def test_route_healthcheckers_readyz(self, api_client: AsyncClient) -> None:
        response = await api_client.get("/healthchecks/readyz")
        response_content = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_content["error"] is False
        assert response_content["message"] == "Successful call to readyz"
