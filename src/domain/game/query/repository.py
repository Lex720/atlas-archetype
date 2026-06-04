from abc import ABC, abstractmethod
from uuid import UUID

from src.infrastructure.database.postgresql.models.game import Game as GameModel


class Game(ABC):
    """Repository abstract class for data query in game model."""

    @abstractmethod
    async def all(self, filters: dict) -> [GameModel]:
        """Abstract method that every class that inherits this needs to implement."""

    @abstractmethod
    async def get(self, uuid: UUID) -> GameModel:
        """Abstract method that every class that inherits this needs to implement."""
