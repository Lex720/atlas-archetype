from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.game.command.entity import Game as GameEntity


class GameCreate(ABC):
    """Usecase abstract class for command data processing in game module."""

    @abstractmethod
    async def execute(self, entity: GameEntity) -> GameEntity:
        """Abstract method that every class that inherits this needs to implement."""


class GameUpdate(ABC):
    """Update game usecase interface for GameEntity."""

    @abstractmethod
    async def execute(self, uuid: UUID, entity: GameEntity) -> GameEntity:
        """Abstract method that every class that inherits this needs to implement."""


class GameDelete(ABC):
    """Delete game usecase interface for GameEntity."""

    @abstractmethod
    async def execute(self, uuid: UUID) -> None:
        """Abstract method that every class that inherits this needs to implement."""
