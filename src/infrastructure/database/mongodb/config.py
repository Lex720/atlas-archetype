from typing import Annotated

from beanie import init_beanie
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.infrastructure.database.mongodb.interface import Mongodb as MongodbInterface
from src.infrastructure.database.mongodb.models.game import Game as GameModel
from src.infrastructure.database.mongodb.settings import get_settings_mongodb

settings = get_settings_mongodb()


class Mongodb(MongodbInterface):
    """Mongodb database configuration with motor async engine.

    Note:
        This class inherit from the Mongodb interface (ABC).
    """

    def __init__(self) -> None:
        """Initialize the class with the necessary objects implemented."""
        self.__client: AsyncIOMotorClient | None = None

    async def connect(self) -> None:
        """Performs the connection to the database.

        Note:
            Create the async client that we used to get the dabatase.

        Returns:
            None.
        """
        self.__client = AsyncIOMotorClient(settings.mongodb_url)
        self.__database = self.__client.get_database(settings.mongodb_database)
        await self._init_beanie()

    async def disconnect(self) -> None:
        """Performs the disconnect from the database.

        Returns:
            None.
        """
        self.__client.close()

    async def get_async_database(self) -> AsyncIOMotorDatabase:
        """Gets async database.

        Returns:
            Async database.
        """
        return self.__database

    async def _init_beanie(self) -> None:
        """Inits Beanie with the defined models

        Returns:
            None.
        """
        await init_beanie(database=self.__database, document_models=[GameModel])


mongodb = Mongodb()

TAsyncSession = Annotated[AsyncIOMotorDatabase, Depends(mongodb.get_async_database)]
