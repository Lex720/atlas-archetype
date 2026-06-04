from typing import TypeVar

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from src.application.commons.data_transform import clean_data_types
from src.infrastructure.broker.rabbitmq.config import rabbitmq
from src.infrastructure.settings import get_settings_global

settings = get_settings_global()

TBase = TypeVar("Base")


class Base:
    """Base class that contains commons functions for business repositories."""

    def __init__(self, database: AsyncIOMotorDatabase) -> TBase:
        """Initialize the class with the necessary objects implemented."""
        self._database = database

    def collection(self) -> AsyncIOMotorCollection:
        """Obtains collection associated to module model"""
        return self._database.get_collection("games")

    async def _prepare_message(self, action: str, model: str, message: dict) -> None:
        """Protected method used to prepare data to publish.

        Args:
            action (:obj:`str`): Command transaction type.
            model (:obj:`str`): Model associated to the data.
            message (:obj:`dict`): Message to be sent into the queue.

        Returns:
            None.
        """
        command_motor = settings.command_motor
        if command_motor == "mongodb":
            message = clean_data_types(message)
            if message.get("_id"):
                del message["_id"]
            message["action"] = action
            message["model"] = model
            await self._publish_to_broker(message)

    async def _publish_to_broker(self, message: dict) -> None:
        """Protected method used to publish data to rabbitmq queue.

        Args:
            message (:obj:`dict`): Message to be sent into the queue.

        Returns:
            None.
        """
        await rabbitmq.publish(message=message)
