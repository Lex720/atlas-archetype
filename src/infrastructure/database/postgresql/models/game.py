from typing import TypeVar

from sqlmodel import Field

from src.infrastructure.database.postgresql.models.base import Base

TBase = TypeVar("Game")


class Game(Base, table=True):
    """Class that contains game model definition."""

    __tablename__ = "games"

    name: str = Field(nullable=False)
    platform: str = Field(nullable=False)
    stock: int = Field(nullable=False)
    price: float = Field(nullable=False)
    active: bool = Field(nullable=False, default=True)
    condition: str = Field(nullable=True)
