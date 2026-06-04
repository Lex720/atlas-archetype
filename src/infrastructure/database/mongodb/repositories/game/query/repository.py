from uuid import UUID

from fastapi_pagination.ext.motor import paginate
from loguru import logger

from src.domain.game.query.repository import Game as GameRepository
from src.infrastructure.database.mongodb.models.game import Game as GameModel
from src.infrastructure.database.mongodb.repositories.base import Base as BaseRepository


class Game(BaseRepository, GameRepository):
    """Game repository implementation for `Game` using mongodb.

    Note:
        This class inherit from the domain game interface (ABC) and base repository.
    """

    async def all(self, filters: dict) -> [dict]:
        """This method encapsulates all data queries for the game collection.

        Note:
            In this layer, we work only with `native` data types and identifiers.

        Args:
            filters (:obj:`class`): Data used to filter results from query.

        Returns:
            Paginated results data in form of a list of dicts for the game collection.
        """
        try:
            return await paginate(
                collection=self.collection(), query_filter=filters, sort={"_id": -1}
            )
        except Exception as e:
            logger.bind(tag="atlas_mongodb_repository_all").error(e)
            raise e

    async def get(self, uuid: UUID) -> dict:
        """This method encapsulates get data queries for the game collection.

        Note:
            In this layer, we work only with `native` data types and identifiers.

        Args:
            uuid (:obj:`uuid`): The unique identifier for the targered instance.

        Returns:
            Result data in form of a dict for the game collection.
        """
        try:
            game = await GameModel.find_one(GameModel.uuid == uuid)
            return game.model_dump() if game else None
        except Exception as e:
            logger.bind(tag="atlas_mongodb_repository_get").error(e)
            raise e
