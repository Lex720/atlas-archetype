from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, PositiveFloat, PositiveInt


class Platform(str, Enum):
    """Allowed options for platform field."""

    playstation = "ps"
    xbox = "xbox"
    pc = "pc"


class Condition(str, Enum):
    """Allowed options for condition field."""

    new = "new"
    used = "used"
    reaconditioned = "reaconditioned"
    defective = "defective"


class Base(BaseModel):
    """Class that represents game model as an entity."""

    name: str
    platform: Platform
    stock: PositiveInt
    price: PositiveFloat
    active: bool
    condition: Condition | None = None
    updated_at: datetime | None = Field(default_factory=datetime.now)
