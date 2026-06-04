from uuid import UUID

from src.domain.game.query.repository import Game as GameRepository
from src.infrastructure.database.postgresql.models.game import Game as GameModel
from src.infrastructure.database.postgresql.repositories.base import (
    Base as BaseRepository,
)


class Game(BaseRepository, GameRepository):
    """Game repository implementation for `Game` using postgresql.

    Note:
        This class inherit from the domain game interface (ABC) and base repository.
    """

    async def all(self, filters: dict) -> [dict]:
        """This method encapsulates all data queries for the game model.

        Note:
            In this layer, we work only with `native` data types and identifiers.

        Args:
            filters (:obj:`class`): Data used to filter results from query.

        Returns:
            Paginated results data in form of a list of dicts for the game model.
        """
        return await self._all(
            model=GameModel,
            filters=filters,
        )

    async def get(self, uuid: UUID) -> dict:
        """This method encapsulates get data queries for the game model.

        Note:
            In this layer, we work only with `native` data types and identifiers.

        Args:
            uuid (:obj:`uuid`): The unique identifier for the targered instance.

        Returns:
            Result data in form of a dict for the game model.
        """
        instance = await self._get(
            model=GameModel,
            filters={"uuid": uuid},
        )
        return instance.model_dump() if instance else {}
