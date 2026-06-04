from pydantic import BaseModel

from src.application.healthcheckers.entity import HealthCheckReport


class LivezResponse(BaseModel):
    """Response scheme of request to livez endpoint."""

    liveness: bool = True


class ReadyzResponse(HealthCheckReport):
    """Response scheme of request to readyz endpoint."""
