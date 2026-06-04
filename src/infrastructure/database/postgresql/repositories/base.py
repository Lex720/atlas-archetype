from typing import TypeVar

from fastapi_pagination.ext.sqlalchemy import paginate
from loguru import logger
from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.commons.data_transform import clean_data_types
from src.infrastructure.broker.rabbitmq.config import rabbitmq
from src.infrastructure.settings import get_settings_global

settings = get_settings_global()

TBase = TypeVar("Base")


class Base:
    """Base class that contains common functions for business repositories."""

    def __init__(self, session: AsyncSession) -> TBase:
        """Initialize the class with the necessary objects implemented."""
        self._session = session

    def _get_filters_parsed(self, model: TBase, filters: dict) -> dict:
        """Protected method used to parsed data to use as filters.

        Args:
            data (:obj:`dict`): Information from the instance model.

        Returns:
            Parsed data in dict form.
        """
        return (getattr(model, key) == value for key, value in filters.items())

    async def _prepare_message(self, action: str, model: str, message: dict) -> None:
        """Protected method used to prepare data to publish.

        Args:
            action (:obj:`str`): Command transaction type.
            model (:obj:`str`): Model associated to the data.
            message (:obj:`dict`): Message to be sent into the queue.

        Returns:
            None.
        """
        command_motor = settings.command_motor
        if command_motor == "postgresql":
            message = clean_data_types(message)
            message["action"] = action
            message["model"] = model
            await self._publish_to_broker(message)

    async def _publish_to_broker(self, message: dict) -> None:
        """Protected method used to publish data to rabbitmq queue.

        Args:
            message (:obj:`dict`): Message to be sent into the queue.

        Returns:
            None.
        """
        await rabbitmq.publish(message=message)

    async def _all(self, model: TBase, filters: dict = None) -> TBase:
        """Protected method used to encapsulate all query action from models.

        Args:
            model (:obj:`class`): Model associated to the data.
            filters (:obj:`dict`): Filters to be used into the query.

        Returns:
            The instances from the database.
        """
        try:
            filters_parsed = self._get_filters_parsed(model, filters) if filters else {}
            query = (
                select(model)
                .where(and_(True, *filters_parsed))
                .order_by(model.created_at.desc())
            )
            return await paginate(self._session, query)
        except Exception as e:
            logger.bind(tag=f"atlas_postgresql_{model.__name__}_all").error(e)
            await self._session.rollback()
            raise e

    async def _get(self, model: TBase, filters: dict) -> TBase:
        """Protected method used to encapsulate get query action from models.

        Args:
            model (:obj:`class`): Model associated to the data.
            filters (:obj:`dict`): Filters to be used into the query.

        Returns:
            The instance from the database.
        """
        try:
            filters_parsed = self._get_filters_parsed(model, filters)
            query = select(model).where(and_(True, True, *filters_parsed))
            query_executed = await self._session.scalars(query)
            return query_executed.first()
        except Exception as e:
            logger.bind(tag=f"atlas_postgresql_{model.__name__}_get").error(e)
            await self._session.rollback()
            raise e

    async def _create(self, model: TBase, data: dict) -> TBase:
        """Protected method used to encapsulate create command action to models.

        Args:
            model (:obj:`class`): Model associated to the data.
            data (:obj:`dict`): Data that needs to be saved.

        Returns:
            The instance from the database.
        """
        try:
            instance = model(**data)
            self._session.add(instance)
            await self._session.commit()
            await self._session.refresh(instance)
            await self._prepare_message(
                "create", str(model.__name__).lower(), instance.model_dump()
            )
            return instance
        except Exception as e:
            logger.bind(tag=f"atlas_postgresql_{model.__name__}_create").error(e)
            await self._session.rollback()
            raise e

    async def _update(self, model: TBase, data: dict, filters: dict) -> TBase:
        """Protected method used to encapsulate update command action to models.

        Args:
            model (:obj:`class`): Model associated to the data.
            data (:obj:`dict`): Data that needs to be saved.
            filters (:obj:`dict`): Filters to be used into the query.

        Returns:
            The instance from the database.
        """
        try:
            filters_parsed = self._get_filters_parsed(model, filters)
            query = update(model).where(and_(True, *filters_parsed)).values(**data)
            await self._session.execute(query)
            await self._session.commit()
            instance = await self._get(model, filters)
            await self._prepare_message(
                "update", str(model.__name__).lower(), instance.model_dump()
            )
            return instance
        except Exception as e:
            logger.bind(tag=f"atlas_postgresql_{model.__name__}_update").error(e)
            await self._session.rollback()
            raise e

    async def _delete(self, model: TBase, filters: dict) -> None:
        """Protected method used to encapsulate delete command action to models.

        Args:
            model (:obj:`class`): Model associated to the data.
            filters (:obj:`dict`): Filters to be used into the query.

        Returns:
            None.
        """
        try:
            filters_parsed = self._get_filters_parsed(model, filters)
            query = delete(model).where(and_(*filters_parsed))
            await self._session.execute(query)
            await self._session.commit()
            await self._prepare_message("delete", str(model.__name__).lower(), filters)
        except Exception as e:
            logger.bind(tag=f"atlas_postgresql_{model.__name__}_delete").error(e)
            await self._session.rollback()
            raise e
