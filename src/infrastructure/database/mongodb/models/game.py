from typing import TypeVar

from beanie import Indexed
from pydantic import Field

from src.infrastructure.database.mongodb.models.base import Base

TBase = TypeVar("Game")


class Game(Base):
    """Class that contains game model definition."""

    name: str = Field(Indexed())
    platform: str = Field(Indexed())
    stock: int = Field()
    price: float = Field()
    active: bool = Field()
    condition: str = Field()

    class Settings:
        name = "games"
        indexes = [
            [
                ("name", 1),
            ],
            [
                ("name", 1),
                ("platform", 1),
            ],
            [
                ("name", 1),
                ("platform", 1),
                ("created_at", 1),
            ],
        ]
