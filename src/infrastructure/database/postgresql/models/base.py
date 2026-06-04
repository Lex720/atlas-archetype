from datetime import datetime
from uuid import UUID

from sqlmodel import Field, SQLModel


class Base(SQLModel):
    """Base class that contains common fields for business models."""

    uuid: UUID = Field(primary_key=True, index=True, nullable=False)
    created_at: datetime = Field(nullable=False)
    updated_at: datetime = Field(nullable=False)
