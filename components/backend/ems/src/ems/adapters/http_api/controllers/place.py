from typing import Annotated, Any

from annotated_types import Gt
from ems.adapters.http_api.auth import get_auth_payload, get_user_role
from ems.adapters.http_api.dependencies import (
    get_auth_service,
    get_place_service,
)
from ems.application import dto
from ems.application.enum import UserRole
from ems.application.services import AuthService, PlaceService
from ems.application.services.place_service import (
    PlaceCreateStatus,
    PlaceDeleteStatus,
    PlaceUpdateStatus,
)
from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Response,
    status,
)

router = APIRouter(prefix="/places", tags=["Места проведения"])


@router.get(
    path="",
    response_model=dto.PlaceListResponse,
    responses={
        200: {"description": "Список мест проведения."},
    },
)
async def get_list(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        place_service: Annotated[PlaceService, Depends(get_place_service)],
        auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
        pagination: Annotated[dto.PaginationParams, Depends()],
):
    user_id = auth_claims.get("user_id", None)
    role = await get_user_role(auth_service, user_id)
    match role:
        case UserRole.ADMIN | UserRole.USER:
            return await place_service.get_list(
                params=pagination,
            )
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error",
            )


@router.get(
    path="/{place_id}",
    response_model=dto.PlaceResponse,
    responses={
        200: {"description": "Информация о местах проведения."},
        400: {"description": "Институт с таким ID не нейден."},
        404: {"description": "Место проведения с таким ID не найдена."},
    },
)
async def get_one(
        place_id: Annotated[int, Gt(0)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
        place_service: Annotated[PlaceService, Depends(get_place_service)],
):
    user_id = auth_claims.get("user_id", None)
    role = await get_user_role(auth_service, user_id)
    match role:
        case UserRole.ADMIN | UserRole.USER:
            place = await place_service.get_by_id(place_id)
            if place is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No place with such id",
                )
            return place
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error",
            )


@router.post(
    path="",
    status_code=201,
    responses={
        201: {"description": "Место проведения создано успешно."},
        404: {"description": "Место проведения не найдено."},
        403: {"description": "Недостаточно прав для действия."},
    },
)
async def add_one(
        response: Response,
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        place_service: Annotated[PlaceService, Depends(get_place_service)],
        auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
        place_data: Annotated[dto.PlaceCreateRequest, Body()],
):
    role = await get_user_role(auth_service, auth_claims.get("user_id", None))
    match role:
        case UserRole.ADMIN:
            match await place_service.add_one(place_data):
                case place_id, PlaceCreateStatus.OK:
                    response.headers["Location"] = f"/place/{place_id}"
                case _:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Unexpected error",
                    )
        case UserRole.USER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden operation for a regular user.",
            )
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error",
            )


@router.put(
    path="",
    responses={
        200: {"description": "Место проведения обновлено успешно."},
        400: {"description": "Факультета с таким ID не найдено."},
        403: {"description": "Недостаточно прав для выполнения действия."},
        404: {"description": "Место проведения не найдено."},
    },
)
async def update_one(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        place_service: Annotated[PlaceService, Depends(get_place_service)],
        auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
        data: Annotated[dto.PlaceUpdateRequest, Body()],
):
    role = await get_user_role(auth_service, auth_claims.get("user_id", None))
    match role:
        case UserRole.ADMIN:
            match await place_service.update_one(data):
                case PlaceUpdateStatus.OK:
                    pass
                case PlaceUpdateStatus.PLACE_NOT_FOUND:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="No place with such id",
                    )
                case PlaceUpdateStatus.INSTITUTION_NOT_FOUND:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="No institution with such id",
                    )
                case _:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Unexpected error",
                    )
        case UserRole.USER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden operation for a regular user.",
            )
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error",
            )


@router.delete(
    path="/{place_id}",
    responses={
        200: {"description": "Место проведения удалено успешно."},
        403: {"description": "Недостаточно прав для выполнения действия."},
    },
)
async def delete_one(
        place_id: Annotated[int, Gt(0)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        place_service: Annotated[PlaceService, Depends(get_place_service)],
        auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
):
    role = await get_user_role(auth_service, auth_claims.get("user_id", None))
    match role:
        case UserRole.ADMIN:
            match await place_service.delete_one(place_id):
                case PlaceDeleteStatus.NOT_FOUND:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="No place with such id",
                    )
                case PlaceDeleteStatus.OK:
                    pass
        case UserRole.USER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden operation for a regular user.",
            )
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error",
            )
