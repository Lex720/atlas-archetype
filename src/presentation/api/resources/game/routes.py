from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from loguru import logger
from fastapi.responses import JSONResponse
from fastapi_pagination import Page

from src.application.game.command.service import game_create as game_create_service
from src.application.game.command.service import game_delete as game_delete_service
from src.application.game.command.service import game_update as game_update_service
from src.application.game.command.usecase import GameCreate as GameCreateUsecase
from src.application.game.command.usecase import GameDelete as GameDeleteUsecase
from src.application.game.command.usecase import GameUpdate as GameUpdateUsecase
from src.application.game.query.service import game_all as game_all_service
from src.application.game.query.service import game_get as game_get_service
from src.application.game.query.usecase import GameAll as GameAllUsecase
from src.application.game.query.usecase import GameGet as GameGetUsecase
from src.domain.game.command.entity import Game as GameEntity
from src.domain.game.command.entity import GameDefaults as GameDefaultsEntity
from src.domain.game.query.entity import GameFilter as GameFilterEntity
from src.presentation.api.commons.dtos import BaseResponse as BaseResponseDTO
from src.presentation.api.resources.game.dtos import (
    GameCreatePayload as GameCreatePayloadDTO,
)
from src.presentation.api.resources.game.dtos import (
    GameCreateResponse as GameCreateResponseDTO,
)
from src.presentation.api.resources.game.dtos import (
    GameDeleteResponse as GameDeleteResponseDTO,
)
from src.presentation.api.resources.game.dtos import (
    GameGetResponse as GameGetResponseDTO,
)
from src.presentation.api.resources.game.dtos import (
    GameUpdatePayload as GameUpdatePayloadDTO,
)
from src.presentation.api.resources.game.dtos import (
    GameUpdateResponse as GameUpdateResponseDTO,
)

game_router = APIRouter(prefix="", tags=["games"])


@game_router.get(
    "/game",
    response_model=Page[GameGetResponseDTO],
    status_code=status.HTTP_200_OK,
)
async def game_all(
    usecase: Annotated[GameAllUsecase, Depends(game_all_service)],
    platform: str | None = None,
) -> Page[GameGetResponseDTO]:
    """Logic for game get all view.

    Note:
        In this layer, we only receive and return `dto` data types.

    Args:
        usecase (:obj:`class`): The implementation for the respective service.
        platform (:obj:`str`, optional): Platform query param.

    Returns:
        Data formatted in the respective response model DTO.
    """
    try:
        filters = {"platform": platform}
        entity = GameFilterEntity(**filters)
        return await usecase.execute(entity)
    except Exception as exc:
        logger.bind(tag="atlas_game_all").error(exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=BaseResponseDTO(
                error=True,
                message="An error occurred processing the request",
                data={},
            ).model_dump(),
        )


@game_router.get(
    "/game/{uuid}",
    response_model=GameGetResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def game_get(
    uuid: UUID,
    usecase: Annotated[GameGetUsecase, Depends(game_get_service)],
) -> GameGetResponseDTO | JSONResponse:
    """Logic for game get one view.

    Note:
        In this layer, we only receive and return `dto` data types.

    Args:
        uuid (:obj:`uuid`): The unique identifier for the targered instance.
        usecase (:obj:`class`): The implementation for the respective service.

    Returns:
        Data formatted in the respective response model DTO.
    """
    try:
        return await usecase.execute(uuid=uuid)
    except Exception as exc:
        logger.bind(tag="atlas_game_get").error(exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=BaseResponseDTO(
                error=True,
                message="An error occurred processing the request",
                data={},
            ).model_dump(),
        )


@game_router.post(
    "/game",
    response_model=GameCreateResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
async def game_create(
    data: GameCreatePayloadDTO,
    usecase: Annotated[GameCreateUsecase, Depends(game_create_service)],
) -> GameCreateResponseDTO | JSONResponse:
    """Logic for game create view.

    Note:
        In this layer, we only receive and return `dto` data types.

    Args:
        data (:obj:`dto`): The base model that contains necessary data.
        usecase (:obj:`class`): The implementation for the respective service.

    Returns:
        Data formatted in the respective response model DTO.
    """
    try:
        entity = GameDefaultsEntity(**data.model_dump())
        return await usecase.execute(entity=entity)
    except Exception as exc:
        logger.bind(tag="atlas_game_create").error(exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=BaseResponseDTO(
                error=True,
                message="An error occurred processing the request",
                data={},
            ).model_dump(),
        )


@game_router.put(
    "/game/{uuid}",
    response_model=GameUpdateResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
async def game_update(
    uuid: UUID,
    data: GameUpdatePayloadDTO,
    usecase: Annotated[GameUpdateUsecase, Depends(game_update_service)],
) -> GameUpdateResponseDTO | JSONResponse:
    """Logic for game update view.

    Note:
        In this layer, we only receive and return `dto` data types.

    Args:
        uuid (:obj:`uuid`): The unique identifier for the targered instance.
        data (:obj:`dto`): The base model that contains necessary data.
        usecase (:obj:`class`): The implementation for the respective service.

    Returns:
        Data formatted in the respective response model DTO.
    """
    try:
        entity = GameEntity(**data.model_dump())
        return await usecase.execute(uuid=uuid, entity=entity)
    except Exception as exc:
        logger.bind(tag="atlas_game_update").error(exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=BaseResponseDTO(
                error=True,
                message="An error occurred processing the request",
                data={},
            ).model_dump(),
        )


@game_router.delete(
    "/game/{uuid}",
    response_model=GameDeleteResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def game_delete(
    uuid: UUID,
    usecase: Annotated[GameDeleteUsecase, Depends(game_delete_service)],
) -> GameDeleteResponseDTO | JSONResponse:
    """Logic for game delete view.

    Note:
        In this layer, we only receive and return `dto` data types.

    Args:
        uuid (:obj:`uuid`): The unique identifier for the targered instance.
        usecase (:obj:`class`): The implementation for the respective service.

    Returns:
        Message with the process result.
    """
    try:
        await usecase.execute(uuid=uuid)
        return {"msg": "Game deleted"}
    except Exception as exc:
        logger.bind(tag="atlas_game_delete").error(exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=BaseResponseDTO(
                error=True,
                message="An error occurred processing the request",
                data={},
            ).model_dump(),
        )
