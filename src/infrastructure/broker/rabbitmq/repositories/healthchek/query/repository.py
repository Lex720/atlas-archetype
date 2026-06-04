from aio_pika import connect_robust
from loguru import logger

from src.application.healthcheckers.interface import CheckRepository
from src.infrastructure.broker.rabbitmq.settings import get_settings_rabbitmq

settings = get_settings_rabbitmq()


class Check(CheckRepository):
    """Check repository implementation for `Check`.

    Note:
        This class inherit from the check repository interface (ABC).
    """

    async def __call__(self) -> bool:
        """This method encapsulates the data query for the check process.

        Returns:
            None.
        """
        try:
            async with await connect_robust(
                host=settings.rabbitmq_host,
                port=settings.rabbitmq_port,
                login=settings.rabbitmq_user,
                password=settings.rabbitmq_password,
                virtualhost=settings.rabbitmq_vhost,
            ):
                return True
        except Exception as e:
            logger.bind(tag="atlas_rabbitmq_check_repository").error(e)
            raise e
