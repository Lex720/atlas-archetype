import asyncio
import signal
import sys

from loguru import logger

sys.path.append("/code/")  # NOTE: do not delete this line, leave it before app imports

from src.infrastructure.broker.rabbitmq.config import rabbitmq  # noqa: E402
from src.infrastructure.database.mongodb.config import mongodb  # noqa: E402
from src.infrastructure.database.postgresql.config import postgresql  # noqa: E402
from src.infrastructure.logger.config import configure_logging  # noqa: E402
from src.infrastructure.settings import get_settings_global  # noqa: E402
from src.presentation.consumer.handlers.etl import replicate_data  # noqa: E402

settings = get_settings_global()


async def startup() -> None:
    """Performs startup process for the consumer.

    Note:
        Configures logger, connects to broker and databases, create task for queue.

    Returns:
        None.
    """
    logger.bind(tag="atlas_startup").info("Configuring logger")
    configure_logging()

    logger.bind(tag="atlas_startup").info("Initializing broker & databases")
    await rabbitmq.connect()
    postgresql.connect()
    await mongodb.connect()

    logger.bind(tag="atlas_startup").info("Initializing consumer")
    await rabbitmq.setup_consumer(handler=replicate_data)

    logger.bind(tag="atlas_startup").info("Initializing loop")
    loop = asyncio.get_running_loop()

    rabbitmq_consume_task = asyncio.create_task(rabbitmq.consume())
    signals = (
        signal.SIGHUP,
        signal.SIGTERM,
        signal.SIGINT,
    )

    def signal_handler() -> asyncio.Task:
        """Creates signal handlers for shutdown process"""
        return asyncio.create_task(shutdown())

    for s in signals:
        loop.add_signal_handler(s, signal_handler)

    logger.bind(tag="atlas_startup").info("Consuming queue")
    await rabbitmq_consume_task

    exit_event = asyncio.Event()
    await exit_event.wait()


async def shutdown() -> None:
    """Performs shutdown process for the consumer.

    Returns:
        None.
    """
    await rabbitmq.disconnect()
    await postgresql.disconnect()
    await mongodb.disconnect()


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(startup())
