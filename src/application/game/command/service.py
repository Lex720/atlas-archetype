from importlib import import_module

from src.application.game.command.usecase import GameCreate as GameCreateUseCase
from src.application.game.command.usecase import GameDelete as GameDeleteUseCase
from src.application.game.command.usecase import GameUpdate as GameUpdateUseCase
from src.infrastructure.settings import get_settings_global

settings = get_settings_global()

command_async_module = import_module(
    "src.infrastructure.database.{}.config".format(settings.command_motor)
)
command_repository_module = import_module(
    "src.infrastructure.database.{}.repositories.game.command.repository".format(
        settings.command_motor
    )
)


CommandAsyncSession = command_async_module.TAsyncSession
GameCommandRepository = command_repository_module.Game


def game_create(db_session: CommandAsyncSession) -> GameCreateUseCase:
    """Return the implementation of game create usecase as a service."""
    return GameCreateUseCase(GameCommandRepository(db_session))


def game_update(db_session: CommandAsyncSession) -> GameUpdateUseCase:
    """Return the implementation of game update usecase as a service."""
    return GameUpdateUseCase(GameCommandRepository(db_session))


def game_delete(db_session: CommandAsyncSession) -> GameDeleteUseCase:
    """Return the implementation of game delete usecase as a service."""
    return GameDeleteUseCase(GameCommandRepository(db_session))
