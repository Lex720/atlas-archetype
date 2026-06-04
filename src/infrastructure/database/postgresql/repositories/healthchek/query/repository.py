from collections.abc import AsyncGenerator

import asyncpg
from loguru import logger

from src.application.healthcheckers.interface import CheckRepository
from src.infrastructure.database.postgresql.settings import get_settings_postgresql

settings = get_settings_postgresql()


async def connect() -> None:
    postgres_dsn = settings.postgresql_url.replace("postgresql+asyncpg", "postgresql")
    timeout = 60.0
    connection = await asyncpg.connect(
        dsn=postgres_dsn,
        timeout=timeout,
    )
    async with connection.transaction(readonly=True):
        return await connection.fetchval("SELECT 1")


async def disconnect(connection: AsyncGenerator | None) -> None:
    await connection.close() if connection and not connection.is_closed() else None


class Check(CheckRepository):
    """Check repository implementation for `Check`.

    Note:
        This class inherit from the check repository interface (ABC).
    """

    async def __call__(self) -> None:
        """This method encapsulates the data query for the check process.

        Returns:
            None.
        """
        connection = None
        try:
            await connect()
        except Exception as e:
            logger.bind(tag="atlas_postgresql_check_repository").error(e)
            raise e
        finally:
            await disconnect(connection)
