from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from loguru import logger

from src.infrastructure.broker.rabbitmq.config import rabbitmq
from src.infrastructure.database.mongodb.config import mongodb
from src.infrastructure.database.postgresql.config import postgresql
from src.infrastructure.logger.config import configure_logging
from src.infrastructure.settings import get_settings_global
from src.presentation.api.commons.exception_handlers import (
    generic_exception_handler,
    not_found_exception_handler,
    validation_error_exception_handler,
)
from src.presentation.api.resources.game.routes import game_router
from src.presentation.api.resources.healthcheckers.routes import healthcheckers_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Manage lifespan events.

    Note:
        Connects/disconnects to databases and broker.

    Returns:
        None.
    """
    logger.bind(tag="lifespan").info("Startup")
    postgresql.connect()
    await mongodb.connect()
    await rabbitmq.connect()
    yield
    logger.bind(tag="lifespan").info("Shutdown")
    await postgresql.disconnect()
    await mongodb.disconnect()
    await rabbitmq.disconnect()


def init_api() -> FastAPI:
    """Initializes the FastAPI application.

    Note:
        Configures logger, add middlewares, includes routers and add exception handlers.

    Returns:
        Configured FastAPI application.
    """
    configure_logging()
    logger.bind(tag="atlas_init_api").info("Configuring logger")

    settings = get_settings_global()

    logger.bind(tag="atlas_init_api").info("Initializing API")
    api = FastAPI(
        lifespan=lifespan,
        openapi_url="/docs/openapi.json",
        docs_url="/docs",
        root_path="/atlas",
    )

    api.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
    common_router_args = {}

    logger.bind(tag="atlas_init_api").info("Including routers")
    api.include_router(game_router, **common_router_args)
    api.include_router(healthcheckers_router, **common_router_args)

    logger.bind(tag="atlas_init_api").info("Add exception handlers")
    api.add_exception_handler(Exception, handler=generic_exception_handler)
    api.add_exception_handler(HTTPException, handler=not_found_exception_handler)
    api.add_exception_handler(
        RequestValidationError, handler=validation_error_exception_handler
    )

    logger.bind(tag="atlas_init_api").info("Adding pagination")
    add_pagination(api)

    return api


api = init_api()
