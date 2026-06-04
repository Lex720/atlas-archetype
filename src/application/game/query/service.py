from importlib import import_module

from src.application.game.query.usecase import GameAll as GameAllUseCase
from src.application.game.query.usecase import GameGet as GameGetUseCase
from src.infrastructure.settings import get_settings_global

settings = get_settings_global()

query_async_module = import_module(
    "src.infrastructure.database.{}.config".format(settings.query_motor)
)
query_repository_module = import_module(
    "src.infrastructure.database.{}.repositories.game.query.repository".format(
        settings.query_motor
    )
)


QueryAsyncSession = query_async_module.TAsyncSession
GameQueryRepository = query_repository_module.Game


def game_all(db_session: QueryAsyncSession) -> GameAllUseCase:
    """Return the implementation of game get all usecase as a service."""
    return GameAllUseCase(GameQueryRepository(db_session))


def game_get(db_session: QueryAsyncSession) -> GameGetUseCase:
    """Return the implementation of game get one usecase as a service."""
    return GameGetUseCase(GameQueryRepository(db_session))
