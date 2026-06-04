from abc import ABC, abstractmethod
from uuid import UUID

from src.infrastructure.database.postgresql.models.game import Game as GameModel


class Game(ABC):
    """Repository abstract class for data command in game model."""

    @abstractmethod
    async def create(self, game_data: dict) -> GameModel:
        """Abstract method that every class that inherits this needs to implement."""

    @abstractmethod
    async def update(self, uuid: UUID, game_data: dict) -> GameModel:
        """Abstract method that every class that inherits this needs to implement."""

    @abstractmethod
    async def delete(self, uuid: UUID) -> None:
        """Abstract method that every class that inherits this needs to implement."""
