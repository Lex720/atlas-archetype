from uuid import UUID

from loguru import logger

from src.domain.game.command.repository import Game as GameRepository
from src.infrastructure.database.mongodb.models.game import Game as GameModel
from src.infrastructure.database.mongodb.repositories.base import Base as BaseRepository


class Game(BaseRepository, GameRepository):
    """Game repository implementation for `Game` using mongodb.

    Note:
        This class inherit from the domain game interface (ABC) and base repository.
    """

    async def create(self, data: dict) -> dict:
        """This method encapsulates the create data commands for the game collection.

        Note:
            In this layer, we work only with `native` data types and identifiers.

        Args:
            data (:obj:`dict`): The dictionary that contains necessary data.

        Returns:
            Created data in form of an dict for the game collection.
        """
        try:
            game = GameModel(**data)
            await game.insert()
            instance = game.model_dump()
        except Exception as e:
            logger.bind(tag="atlas_mongodb_repository_create").error(e)
            raise e
        await self._prepare_message("create", "game", instance)
        return instance

    async def update(self, uuid: UUID, data: dict) -> dict:
        """This method encapsulates the update data commands for the game collection.

        Note:
            In this layer, we work only with `native` data types and identifiers.

        Args:
            uuid (:obj:`uuid`): The unique identifier for the targered instance.
            data (:obj:`dict`): The dictionary that contains necessary data.

        Returns:
            Updated data in form of an dict for the game collection.
        """
        try:
            game = await GameModel.find_one(GameModel.uuid == uuid)
            if not game:
                return {}
            await game.update({"$set": data})
            instance = game.model_dump() if game else None
        except Exception as e:
            logger.bind(tag="atlas_mongodb_repository_update").error(e)
            raise e
        await self._prepare_message("update", "game", instance)
        return instance

    async def delete(self, uuid: UUID) -> None:
        """This method encapsulates the delete data commands for the game collection.

        Note:
            In this layer, we work only with `native` data types and identifiers.

        Args:
            uuid (:obj:`uuid`): The unique identifier for the targered instance.

        Returns:
            None.
        """
        try:
            game = await GameModel.find_one(GameModel.uuid == uuid)
            if not game:
                return None
            await game.delete()
        except Exception as e:
            logger.bind(tag="atlas_mongodb_repository_delete").error(e)
            raise e
        await self._prepare_message("delete", "game", {"uuid": str(uuid)})
