from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from asgi_lifespan import LifespanManager

from src.presentation.api.main import api
from src.infrastructure.broker.rabbitmq.config import rabbitmq
from src.presentation.consumer.handlers.etl import replicate_data


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def api_client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=api, raise_app_exceptions=True)
    async with LifespanManager(api):
        async with AsyncClient(
            transport=transport, base_url="http://localhost:8081"
        ) as client:
            yield client


@pytest_asyncio.fixture(scope="session", autouse=True, loop_scope="session")
async def consumer_broker() -> AsyncGenerator:
    await rabbitmq.setup_consumer(handler=replicate_data)
    await rabbitmq.consume()
    yield
    await rabbitmq.disconnect()
