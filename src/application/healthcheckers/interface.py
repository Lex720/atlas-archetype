from abc import ABC, abstractmethod

from src.application.healthcheckers.entity import CheckResult


class CheckRepository(ABC):
    """Repository abstract class for data query in health checks."""

    @abstractmethod
    async def __call__(self) -> bool:
        """Abstract method that every class that inherits this needs to implement."""


class CheckUsecase(ABC):
    """Usecase abstract class for data processing in health checks."""

    @abstractmethod
    async def __call__(self) -> CheckResult:
        """Abstract method that every class that inherits this needs to implement."""
