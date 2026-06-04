from datetime import datetime
from uuid import UUID, uuid4

from pydantic import Field, model_validator

from src.domain.game.base.entity import Base, Condition


class Game(Base):
    """Class that represents game model as an entity."""

    @model_validator(mode="after")
    def valid_active(self) -> "Game":
        """This method perform a business validation using two fields from the model.

        Note:
            The game can not be active if the condition is `defective`.

        Returns:
            The original data from the entity.
        """
        if self.active and self.condition == Condition.defective:
            raise ValueError(
                "You can't mark a product active if it has defective condition"
            )
        return self


class GameDefaults(Base):
    """Game represents game as an entity (only for creation)."""

    uuid: UUID | None = Field(default_factory=uuid4)
    created_at: datetime | None = Field(default_factory=datetime.now)
