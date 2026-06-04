from abc import ABC, abstractmethod


class RabbitMQ(ABC):
    """Client abstract class for rabbitmq broker configuration."""

    @abstractmethod
    async def connect(self) -> None:
        """Abstract method that every class that inherits this needs to implement."""

    @abstractmethod
    async def setup_consumer(self) -> None:
        """Abstract method that every class that inherits this needs to implement."""

    @abstractmethod
    async def publish(self) -> None:
        """Abstract method that every class that inherits this needs to implement."""

    @abstractmethod
    async def consume(self) -> None:
        """Abstract method that every class that inherits this needs to implement."""

    @abstractmethod
    async def disconnect(self) -> None:
        """Abstract method that every class that inherits this needs to implement."""
