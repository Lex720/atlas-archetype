from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.game.query.entity import Game as GameEntity


class GameAll(ABC):
    """Usecase abstract class for query data processing in game module."""

    @abstractmethod
    async def execute(self) -> GameEntity:
        """Abstract method that every class that inherits this needs to implement."""


class GameGet(ABC):
    """Get game usecase interface for GameEntity."""

    @abstractmethod
    async def execute(self, uuid: UUID) -> GameEntity:
        """Abstract method that every class that inherits this needs to implement."""
