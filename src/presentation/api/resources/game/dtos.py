from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


# Bases
class GameBasePayload(BaseModel):
    """Payload basic scheme for command endpoints."""

    name: str
    platform: str
    stock: int
    price: int
    active: bool | None
    condition: str | None = None


class GameBaseResponse(GameBasePayload):
    """Response basic scheme for query endpoints."""

    uuid: UUID
    created_at: datetime
    updated_at: datetime


# Payloads
class GameCreatePayload(GameBasePayload):
    """Payload game create scheme."""

    pass


class GameUpdatePayload(GameBasePayload):
    """Payload game update scheme."""

    pass


# Responses
class GameGetResponse(GameBaseResponse):
    """Response game get scheme."""

    pass


class GameCreateResponse(GameBaseResponse):
    """Response game create scheme."""

    pass


class GameUpdateResponse(GameBaseResponse):
    """Response game update scheme."""

    pass


class GameDeleteResponse(BaseModel):
    """Response game delete scheme."""

    msg: str
