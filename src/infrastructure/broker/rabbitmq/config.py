import json
from typing import Callable

from aio_pika import ExchangeType, IncomingMessage
from aio_pika import Message as AioPikaMessage
from aio_pika import RobustChannel, RobustConnection, connect_robust
from aio_pika.abc import AbstractExchange, AbstractQueue
from loguru import logger

from src.infrastructure.broker.rabbitmq.interface import RabbitMQ as RabbitMQInterface
from src.infrastructure.broker.rabbitmq.settings import get_settings_rabbitmq

settings = get_settings_rabbitmq()


class RabbitMQ(RabbitMQInterface):
    """RabbitMQ broker configuration with aio pika.

    Note:
        This class inherit from the RabbitMQ interface (ABC).
    """

    def __init__(self) -> None:
        """Initialize the class with the necessary objects implemented."""
        self.__host = settings.rabbitmq_host
        self.__port = settings.rabbitmq_port
        self.__user = settings.rabbitmq_user
        self.__password = settings.rabbitmq_password
        self.__vhost = settings.rabbitmq_vhost

        self.__connection: RobustConnection | None = None
        self.__channel: RobustChannel | None = None
        self.__handler: Callable | None = None
        self.__queue_name = settings.rabbitmq_queue_name
        self.__queue: AbstractQueue | None = None
        self.__queue_delay: AbstractQueue | None = None
        self.__queue_delay_dlq: AbstractQueue | None = None
        self.__delay_exchange: AbstractExchange | None = None

        self.__prefetch_count = settings.rabbitmq_prefetch_count
        self.__delay_ms = settings.rabbitmq_delay_ms
        self.__max_retries = settings.rabbitmq_max_retries

    async def connect(self) -> None:
        """Performs the connection to the broker.

        Note:
            Create the async engine that needs to be used to generate the async session.

        Returns:
            None.
        """
        self.__connection = await connect_robust(
            host=self.__host,
            port=self.__port,
            login=self.__user,
            password=self.__password,
            virtualhost=self.__vhost,
        )
        self.__channel = await self.__connection.channel()
        await self.__channel.set_qos(prefetch_count=self.__prefetch_count)

    async def setup_consumer(self, handler: Callable) -> None:
        """Configure consumer: set handler, exchange, queue, delay and dlq.

        Note:
            Queue type MUST be `quorum`.

        Args:
            handler (:obj:`call`): Function in charge of process received messages.

        Returns:
            None.
        """
        await self.connect()
        self.__handler = handler
        self.__queue = await self.__channel.declare_queue(
            name=self.__queue_name, durable=True, arguments={"x-queue-type": "quorum"}
        )
        self.__delay_exchange = await self.__channel.declare_exchange(
            name=f"{self.__queue_name}.delayed_exchange",
            type=ExchangeType.X_DELAYED_MESSAGE,
            durable=True,
            arguments={"x-delayed-type": "direct", "x-queue-type": "quorum"},
        )
        self.__queue_delay = await self.__channel.declare_queue(
            name=f"{self.__queue_name}.delay",
            durable=True,
            arguments={"x-queue-type": "quorum"},
        )
        await self.__queue_delay.bind(
            exchange=self.__delay_exchange,
            routing_key=f"{self.__queue_name}.routing_delay",
        )
        self.__queue_delay_dlq = await self.__channel.declare_queue(
            name=f"{self.__queue_name}.delay_dlq",
            durable=True,
            arguments={"x-queue-type": "quorum"},
        )
        await self.__queue_delay_dlq.bind(
            exchange=self.__delay_exchange,
            routing_key=f"{self.__queue_name}.routing_delay_dlq",
        )

    async def publish(self, message: dict) -> None:
        """Encodes and publish message to regular queue.

        Args:
            message (:obj:`dict`): Message content.

        Returns:
            None.
        """
        assert self.__channel is not None, "The RabbitMQBroker has not been configured"
        encoded_message = AioPikaMessage(body=json.dumps(message).encode("utf-8"))
        await self.__channel.default_exchange.publish(
            encoded_message,
            routing_key=self.__queue_name,
        )

    async def consume(self) -> None:
        """Consume message from queues.

        Note:
            Queue off for `dlq`.

        Usage::
            await self.___queue_delay_dlq.consume(self.__process_message, no_ack=False)

        Returns:
            None.
        """
        await self.__queue.consume(self.__process_message, no_ack=False)
        await self.__queue_delay.consume(self.__process_message, no_ack=False)
        # await self.___queue_delay_dlq.consume(self.__process_message, no_ack=False)

    async def __process_message(self, message: IncomingMessage) -> None:
        """Processes consumed messages with no auto acknowledge.

        Note:
            Here we configure retries, delay time between messages and exchanges.

        Args:
            message (:obj:`message`): The aio pika encoded message.

        Returns:
            None.
        """
        async with message.process():
            data = json.loads(message.body.decode("utf-8"))

            try:
                success = await self.__handler(data=data)
            except Exception as e:
                logger.bind(tag="atlas_rabbitmq_process_message").error(
                    f"Handler raised an exception for message in queue {self.__queue_name}: {e}"
                )
                success = False

            if success:
                return

            retries = message.properties.headers.get("retries", 0)
            exceeded_retries = retries >= self.__max_retries

            if exceeded_retries:
                logger.bind(tag="atlas_rabbitmq_process_message").warning(
                    f"""
                    Message processing in queue {self.__queue_name} was unsuccessful
                    and exhausted the number of retries {self.__max_retries}.
                    Redirecting message to DLQ, please review.
                    """
                )
                await self.__send_message_to_dlq(message)
                return

            self.__add_retries_to_message(message)
            await self.__send_message_to_delay(message)

    def __add_retries_to_message(self, message: IncomingMessage) -> None:
        """Add retries to message headers property and set delay time.

        Args:
            message (:obj:`message`): The aio pika encoded message.

        Returns:
            None.
        """
        retries = message.properties.headers.get("retries", 0)
        message.properties.headers["retries"] = retries + 1
        message.properties.headers["x-delay"] = (
            message.properties.headers["retries"] * self.__delay_ms
        )

    async def __send_message_to_delay(self, message: IncomingMessage) -> None:
        """Exanges message through routing key to delay queue.

        Args:
            message (:obj:`message`): The aio pika encoded message.

        Returns:
            None.
        """
        await self.__delay_exchange.publish(
            message, routing_key=f"{self.__queue_name}.routing_delay"
        )

    async def __send_message_to_dlq(self, message: IncomingMessage) -> None:
        """Exanges message through routing key to dlq.

        Args:
            message (:obj:`message`): The aio pika encoded message.

        Returns:
            None.
        """
        await self.__delay_exchange.publish(
            message, routing_key=f"{self.__queue_name}.routing_delay_dlq"
        )

    async def disconnect(self) -> None:
        """Performs the disconnect from the broker.

        Returns:
            None.
        """
        if self.__connection is not None:
            await self.__channel.close()
            await self.__connection.close()


rabbitmq = RabbitMQ()
