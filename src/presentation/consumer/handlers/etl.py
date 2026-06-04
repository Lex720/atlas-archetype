import uuid

from fast_depends import inject
from fast_depends.pydantic import PydanticSerializer
from loguru import logger

from src.application.game.command.usecase import GameCreate as GameCreateUseCase
from src.application.game.command.usecase import GameDelete as GameDeleteUseCase
from src.application.game.command.usecase import GameUpdate as GameUpdateUseCase
from src.domain.game.command.entity import Game as GameEntity
from src.domain.game.command.entity import GameDefaults as GameDefaultsEntity
from src.infrastructure.database.mongodb.config import mongodb
from src.infrastructure.database.mongodb.repositories.game.command.repository import (
    Game as GameCommandRepositoryMongodb,
)
from src.infrastructure.database.postgresql.config import postgresql
from src.infrastructure.database.postgresql.repositories.game.command.repository import (  # noqa: E501
    Game as GameCommandRepositoryPostgresql,
)
from src.infrastructure.settings import get_settings_global

ENGINES_MAP = {"postgresql": mongodb, "mongodb": postgresql}

REPOSITORIES_MAP = {
    "game": {
        "postgresql": GameCommandRepositoryMongodb,
        "mongodb": GameCommandRepositoryPostgresql,
    }
}

USECASES_MAP = {
    "game": {
        "create": GameCreateUseCase,
        "update": GameUpdateUseCase,
        "delete": GameDeleteUseCase,
    }
}

ENTITIES_MAP = {"game": {"create": GameDefaultsEntity, "update": GameEntity}}


@inject(serializer=PydanticSerializer())
async def replicate_data(data: dict) -> bool:
    """Handler in charge of data replication between databases.

    Note:
        This is a unique handlers that embrace all models.

    Args:
        data (:obj:`dict`): Data to replicate.

    Returns:
        True if successful, error otherwise.
    """
    logger.bind(tag="atlas_handler_replicate_data").info(f"Processing {data}")

    action = data.pop("action", None)
    model = data.pop("model", None)

    if not action or not model:
        logger.bind(tag="atlas_handler_replicate_data").error(
            f"Missing required fields 'action' or 'model' in message: {data}"
        )
        return False

    command_motor = get_settings_global().command_motor

    engine = ENGINES_MAP.get(command_motor)
    db_session = await engine.get_async_database()

    model_repositories = REPOSITORIES_MAP.get(model)
    if not model_repositories:
        logger.bind(tag="atlas_handler_replicate_data").error(
            f"Unknown model '{model}' — no repository registered"
        )
        return False

    repository_class = model_repositories.get(command_motor)
    usecase_class = USECASES_MAP.get(model, {}).get(action)
    entity_class = ENTITIES_MAP.get(model, {}).get(action)

    if not repository_class or not usecase_class:
        logger.bind(tag="atlas_handler_replicate_data").error(
            f"No handler registered for model='{model}' action='{action}' motor='{command_motor}'"
        )
        return False

    usecase = usecase_class(repository_class(db_session))
    entity = entity_class(**data) if entity_class else None

    if action == "create":
        await usecase.execute(entity=entity)
    if action == "update":
        await usecase.execute(uuid.UUID(data.get("uuid")), entity=entity)
    if action == "delete":
        await usecase.execute(uuid.UUID(data.get("uuid")))

    return True
