from typing import Dict, List

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.presentation.api.commons.dtos import BaseResponse as BaseResponseDTO


async def generic_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """Configures the default handler for generic exceptions

    Returns:
        Json response with properly information for the exception.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=BaseResponseDTO[Dict](
            error=True, message=exc.detail, data={}
        ).model_dump(),
    )


async def not_found_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    """Configures the default handler for not found exceptions

    Returns:
        Json response with properly information about the exception.
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=BaseResponseDTO[Dict](
            error=True, message=exc.detail, data={}
        ).model_dump(),
    )


async def validation_error_exception_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    """Configures the default handler for not validation error exceptions

    Returns:
        Json response with properly information about the exception.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=BaseResponseDTO[List](
            error=True, message="Errors ocurred during validation", data=exc.errors()
        ).model_dump(),
    )
