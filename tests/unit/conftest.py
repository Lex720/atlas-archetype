from collections.abc import AsyncGenerator
from http import HTTPStatus

import pytest_asyncio
from fastapi import HTTPException
from httpx import ASGITransport, AsyncClient
from pydantic import BaseModel

from src.presentation.api.main import api


class _BodySchema(BaseModel):
    test_property: str


async def _generate_422(body: _BodySchema) -> None:
    pass


async def _generate_500() -> None:
    raise HTTPException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Internal server error"
    )


async def _generate_404() -> None:
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Not found")


@pytest_asyncio.fixture(scope="session")
async def api_client() -> AsyncGenerator[AsyncClient, None]:
    api.add_api_route("/500", endpoint=_generate_500)
    api.add_api_route("/404", endpoint=_generate_404)
    api.add_api_route("/422", endpoint=_generate_422, methods=["post"])
    transport = ASGITransport(app=api, raise_app_exceptions=False)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
