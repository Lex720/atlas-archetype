from uuid import UUID

from src.domain.game.command.repository import Game as GameRepository
from src.infrastructure.database.postgresql.models.game import Game as GameModel
from src.infrastructure.database.postgresql.repositories.base import (
    Base as BaseRepository,
)


class Game(BaseRepository, GameRepository):
    """Game repository implementation for `Game` using postgresql.

    Note:
        This class inherit from the domain game interface (ABC) and base repository.
    """

    async def create(self, data: dict) -> dict:
        """This method encapsulates the create data commands for the game model.

        Note:
            In this layer, we work only with `native` data types and identifiers.

        Args:
            data (:obj:`dict`): The dictionary that contains necessary data.

        Returns:
            Created data in form of an dict for the game model.
        """
        instance = await self._create(
            model=GameModel,
            data=data,
        )
        return instance.model_dump() if instance else {}

    async def update(self, uuid: UUID, data: dict) -> dict:
        """This method encapsulates the update data commands for the game model.

        Note:
            In this layer, we work only with `native` data types and identifiers.

        Args:
            uuid (:obj:`uuid`): The unique identifier for the targered instance.
            data (:obj:`dict`): The dictionary that contains necessary data.

        Returns:
            Updated data in form of an dict for the game model.
        """
        instance = await self._update(
            model=GameModel,
            data=data,
            filters={"uuid": uuid},
        )
        return instance.model_dump() if instance else {}

    async def delete(self, uuid: UUID) -> None:
        """This method encapsulates the delete data commands for the game model.

        Note:
            In this layer, we work only with `native` data types and identifiers.

        Args:
            uuid (:obj:`uuid`): The unique identifier for the targered instance.

        Returns:
            None.
        """
        return await self._delete(
            model=GameModel,
            filters={"uuid": uuid},
        )
