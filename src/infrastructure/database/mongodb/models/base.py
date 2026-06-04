from datetime import datetime
from uuid import UUID

from beanie import Document, Indexed
from pydantic import Field


class Base(Document):
    """Base class that contains common fields for business models."""

    uuid: UUID = Field()
    created_at: datetime = Field(Indexed())
    updated_at: datetime = Field()
