from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.application.healthcheckers.service import health_check as health_check_service
from src.application.healthcheckers.usecase import HealthCheck as HealthCheckUseCase
from src.presentation.api.commons.dtos import BaseResponse as BaseResponseDTO
from src.presentation.api.resources.healthcheckers.dtos import (
    LivezResponse as LivezResponseDTO,
)
from src.presentation.api.resources.healthcheckers.dtos import (
    ReadyzResponse as ReadyzResponseDTO,
)

healthcheckers_router = APIRouter(prefix="/healthchecks", tags=["healthchecks"])


@healthcheckers_router.get(
    "/livez",
    response_model=BaseResponseDTO[LivezResponseDTO],
    status_code=status.HTTP_200_OK,
)
def get_liveness() -> BaseResponseDTO:
    """Logic for get liveness check.

    Returns:
        Data formatted in the respective response model DTO.
    """
    return BaseResponseDTO(
        error=False,
        message="Successful call to livez",
        data={"liveness": True},
    )


@healthcheckers_router.get(
    "/readyz",
    response_model=BaseResponseDTO[ReadyzResponseDTO],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": BaseResponseDTO[ReadyzResponseDTO]
        }
    },
)
async def get_readiness(
    health_check_service: Annotated[HealthCheckUseCase, Depends(health_check_service)],
) -> JSONResponse:
    """Logic for get readiness check.

    Returns:
        Data formatted in the respective response model DTO.
    """
    health_check_report = await health_check_service()

    status_code = (
        status.HTTP_200_OK
        if health_check_report.healthy
        else status.HTTP_503_SERVICE_UNAVAILABLE
    )

    content = BaseResponseDTO(
        error=not health_check_report.healthy,
        message="Successful call to readyz",
        data=health_check_report,
    ).model_dump()

    return JSONResponse(status_code=status_code, content=content)
