from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from src.application.healthcheckers.interface import CheckRepository
from src.infrastructure.database.mongodb.settings import get_settings_mongodb

settings = get_settings_mongodb()


async def connect() -> None:
    await (
        AsyncIOMotorClient(settings.mongodb_url)
        .get_database("test")
        .command({"ping": 1})
    )


async def disconnect(client: AsyncIOMotorClient) -> None:
    client.close() if client else None


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
        client = None
        try:
            await connect()
        except Exception as e:
            logger.bind(tag="atlas_mongodb_check_repository").error(e)
            raise e
        finally:
            await disconnect(client)
