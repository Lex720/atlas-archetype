from uuid import UUID

from src.domain.game.exception import GameNotFoundError
from src.domain.game.query.entity import Game as GameEntity
from src.domain.game.query.entity import GameFilter as GameFilterEntity
from src.domain.game.query.repository import Game as GameRepository
from src.domain.game.query.usecase import GameAll as GameAllUsecase
from src.domain.game.query.usecase import GameGet as GameGetUsecase


class GameAll(GameAllUsecase):
    """Get all games usecase implementation for `GameEntity`.

    Note:
        This class inherit from the domain game all interface (ABC).
    """

    def __init__(self, repository: GameRepository) -> None:
        """Initialize the class with the necessary objects implemented.

        Args:
            repository (:obj:`class`): The query repository for game module.
        """
        self.repository = repository

    async def execute(self, entity: GameFilterEntity) -> GameEntity:
        """This method encapsulates all the business logic for the game all usecase.

        Note:
            In the usecase layer, we work only with `entity` data types and identifiers.

        Args:
            entity (:obj:`class`): The entity instance to filter results from query.

        Returns:
            Paginated results in form of a list of entities for the game model.
        """
        return await self.repository.all(entity.model_dump(exclude_none=True))


class GameGet(GameGetUsecase):
    """Get game usecase implementation for `GameEntity`.

    Note:
        This class inherit from the domain game get interface (ABC).
    """

    def __init__(self, repository: GameRepository) -> None:
        """Initialize the class with the necessary objects implemented.

        Args:
            repository (:obj:`class`): The query repository for game module.
        """
        self.repository = repository

    async def execute(self, uuid: UUID) -> GameEntity:
        """This method encapsulates all the business logic for the game get usecase.

        Note:
            In the usecase layer, we work only with `entity` data types and identifiers.

        Args:
            uuid (:obj:`uuid`): The unique identifier for the targered instance.

        Returns:
            Result data in form of a entity for the game model.
        """
        instance_dict = await self.repository.get(uuid)
        if not instance_dict:
            raise GameNotFoundError
        return GameEntity(**instance_dict)
