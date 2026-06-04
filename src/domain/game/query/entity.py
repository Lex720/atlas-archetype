from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.domain.game.base.entity import Base, Platform


class Game(Base):
    """Class that represents game model as an entity."""

    uuid: UUID
    created_at: datetime


class GameFilter(BaseModel):
    """Class that represents game filter model as an entity."""

    platform: Platform | None
