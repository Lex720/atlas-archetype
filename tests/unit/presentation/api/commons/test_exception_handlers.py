import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestExceptionHandlers:
    async def test_generic_exception_handler(self, api_client: AsyncClient) -> None:
        response = await api_client.get("/500")
        response_content = response.json()

        assert response_content["error"] is True
        assert response_content["message"] == "Internal server error"
        assert response_content["data"] == {}

    async def test_not_found_exception_handler(self, api_client: AsyncClient) -> None:
        response = await api_client.get("/404")
        response_content = response.json()

        assert response_content["error"] is True
        assert response_content["message"] == "Not found"
        assert response_content["data"] == {}

    async def test_validation_error_exception_handler(
        self, api_client: AsyncClient
    ) -> None:
        response = await api_client.post("/422", json={})
        response_content = response.json()

        assert response_content["error"] is True
        assert response_content["message"] == "Errors ocurred during validation"
