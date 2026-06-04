from uuid import UUID

from src.domain.game.command.entity import Game as GameCommandEntity
from src.domain.game.command.repository import Game as GameRepository
from src.domain.game.command.usecase import GameCreate as GameCreateUsecase
from src.domain.game.command.usecase import GameDelete as GameDeleteUsecase
from src.domain.game.command.usecase import GameUpdate as GameUpdateUsecase
from src.domain.game.exception import GameNotFoundError
from src.domain.game.query.entity import Game as GameQueryEntity


class GameCreate(GameCreateUsecase):
    """Create game usecase implementation for `GameEntity`.

    Note:
        This class inherit from the domain game create interface (ABC).
    """

    def __init__(self, repository: GameRepository) -> None:
        """Initialize the class with the necessary objects implemented.

        Args:
            repository (:obj:`class`): The command repository for game module.
        """
        self.repository = repository

    async def execute(self, entity: GameCommandEntity) -> GameQueryEntity:
        """This method encapsulates all the business logic for the game create usecase.

        Note:
            In the usecase layer, we work only with `entity` data types and identifiers.

        Args:
            entity (:obj:`class`): The entity instance that contains necessary data.

        Returns:
            Created data in form of an entity for the game model.
        """
        instance_dict = await self.repository.create(
            entity.model_dump(exclude_none=True)
        )
        if not instance_dict:
            raise GameNotFoundError
        return GameQueryEntity(**instance_dict)


class GameUpdate(GameUpdateUsecase):
    """Update game usecase implementation for `GameEntity`.

    Note:
        This class inherit from the domain game update interface (ABC).
    """

    def __init__(self, repository: GameRepository) -> None:
        """Initialize the class with the necessary objects implemented.

        Args:
            repository (:obj:`class`): The command repository for game module.
        """
        self.repository = repository

    async def execute(self, uuid: UUID, entity: GameCommandEntity) -> GameQueryEntity:
        """This method encapsulates all the business logic for the game update usecase.

        Note:
            In the usecase layer, we work only with `entity` data types and identifiers.

        Args:
            uuid (:obj:`uuid`): The unique identifier for the targered instance.
            entity (:obj:`class`): The entity instance that contains necessary data.

        Returns:
            Updated data in form of an entity for the game model.
        """
        instance_dict = await self.repository.update(
            uuid, entity.model_dump(exclude_defaults=True)
        )
        if not instance_dict:
            raise GameNotFoundError
        return GameQueryEntity(**instance_dict)


class GameDelete(GameDeleteUsecase):
    """Delete game usecase implementation for `GameEntity`.

    Note:
        This class inherit from the domain game delete interface (ABC).
    """

    def __init__(self, repository: GameRepository) -> None:
        """Initialize the class with the necessary objects implemented.

        Args:
            repository (:obj:`class`): The command repository for game module.
        """
        self.repository = repository

    async def execute(self, uuid: UUID) -> None:
        """This method encapsulates all the business logic for the game delete usecase.

        Note:
            In the usecase layer, we work only with `entity` data types and identifiers.

        Args:
            uuid (:obj:`uuid`): The unique identifier for the targered instance.

        Returns:
            None.
        """
        return await self.repository.delete(uuid)
