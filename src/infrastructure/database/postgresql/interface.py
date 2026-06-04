from abc import ABC, abstractmethod


class Postgresql(ABC):
    """Client abstract class for mongodb database configuration."""

    @abstractmethod
    async def connect(self) -> None:
        """Abstract method that every class that inherits this needs to implement."""

    @abstractmethod
    async def disconnect(self) -> None:
        """Abstract method that every class that inherits this needs to implement."""

    @abstractmethod
    async def get_async_session(self) -> None:
        """Abstract method that every class that inherits this needs to implement."""

    @abstractmethod
    async def get_async_database(self) -> None:
        """Abstract method that every class that inherits this needs to implement."""
