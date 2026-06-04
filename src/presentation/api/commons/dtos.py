from typing import Generic, TypeVar

from pydantic import BaseModel

DataType = TypeVar("DataType")


class BaseResponse(BaseModel, Generic[DataType]):
    """Response scheme of request to generic response."""

    error: bool
    message: str
    data: DataType
