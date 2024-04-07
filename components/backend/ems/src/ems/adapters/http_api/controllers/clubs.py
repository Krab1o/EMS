from typing import Annotated, Any

from annotated_types import Gt
from ems.adapters.http_api.auth import get_auth_payload, get_user_role
from ems.adapters.http_api.dependencies import (
    get_auth_service,
    get_club_service,
)
from ems.application import dto
from ems.application.enum import UserRole
from ems.application.services import AuthService, ClubService
from ems.application.services.club_service import (
    ClubCreateStatus,
    ClubDeleteStatus,
    ClubUpdateStatus,
)
from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Response,
    status,
)

router = APIRouter(prefix="/clubs", tags=["Секции"])


@router.get(
    path="",
    response_model=dto.ClubListResponse,
    responses={
        200: {"description": "Список секций."},
    },
)
async def get_list(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    club_service: Annotated[ClubService, Depends(get_club_service)],
    auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
    pagination: Annotated[dto.PaginationParams, Depends()],
):
    role = await get_user_role(auth_service, auth_claims.get("user_id", None))
    match role:
        case UserRole.ADMIN | UserRole.USER:
            return await club_service.get_list(
                params=pagination,
            )
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error",
            )


@router.get(
    path="/{club_id}",
    response_model=dto.ClubResponse,
    responses={
        200: {"description": "Информация о секции."},
        404: {"description": "Секция с таким ID не найдена."},
    },
)
async def get_one(
    club_id: Annotated[int, Gt(0)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
    club_service: Annotated[ClubService, Depends(get_club_service)],
):
    role = await get_user_role(auth_service, auth_claims.get("user_id", None))
    match role:
        case UserRole.ADMIN | UserRole.USER:
            club = await club_service.get_by_id(
                club_id=club_id,
            )

            if club is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No club with such id",
                )
            return club
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error",
            )


@router.post(
    path="",
    status_code=201,
    responses={
        201: {"description": "Секция создана успешно."},
        404: {"description": "Секция не найдена."},
        403: {"description": "Недостаточно прав для действия."},
    },
)
async def add_one(
    response: Response,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    club_service: Annotated[ClubService, Depends(get_club_service)],
    auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
    club_data: Annotated[dto.ClubCreateRequest, Body()],
):
    role = await get_user_role(auth_service, auth_claims.get("user_id", None))
    match role:
        case UserRole.ADMIN:
            match await club_service.add_one(club_data):
                case club_id, ClubCreateStatus.OK:
                    response.headers["Location"] = f"/clubs/{club_id}"
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
        200: {"description": "Секция обновлена успешно."},
        403: {"description": "Недостаточно прав для выполнения действия."},
        404: {"description": "Секция не найдена."},
    },
)
async def update_one(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    club_service: Annotated[ClubService, Depends(get_club_service)],
    auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
    data: Annotated[dto.ClubUpdateRequest, Body()],
):
    role = await get_user_role(auth_service, auth_claims.get("user_id", None))
    match role:
        case UserRole.ADMIN:
            match await club_service.update_one(data):
                case ClubUpdateStatus.OK:
                    pass
                case ClubUpdateStatus.NOT_FOUND:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="No event type with such id",
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
    path="/{club_id}",
    responses={
        200: {"description": "Секция удалена успешно."},
        403: {"description": "Недостаточно прав для выполнения действия."},
    },
)
async def delete_one(
    club_id: Annotated[int, Gt(0)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    club_service: Annotated[ClubService, Depends(get_club_service)],
    auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
):
    role = await get_user_role(auth_service, auth_claims.get("user_id", None))
    match role:
        case UserRole.ADMIN:
            match await club_service.delete_one(club_id):
                case ClubDeleteStatus.NOT_FOUND:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="No event type with such id",
                    )
                case ClubDeleteStatus.OK:
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
