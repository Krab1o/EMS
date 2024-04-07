from typing import Annotated, Any

from annotated_types import Gt
from ems.adapters.http_api.auth import get_auth_payload, get_user_role
from ems.adapters.http_api.dependencies import (
    get_auth_service,
    get_user_service,
)
from ems.application import dto
from ems.application.enum import UserRole
from ems.application.services import AuthService, UserService
from ems.application.services.user_service import (
    UserCreateStatus,
    UserDeleteStatus,
    UserUpdateStatus,
)
from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Response,
    status,
)
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get(
    path="",
    response_model=dto.UserListResponse,
    responses={
        200: {"description": "Список пользователей."},
    },
)
async def get_list(
    user_service: Annotated[UserService, Depends(get_user_service)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
    pagination: Annotated[dto.PaginationParams, Depends()],
):
    role = await get_user_role(auth_service, auth_claims.get("user_id", None))
    match role:
        case UserRole.ADMIN:
            users = await user_service.get_list(params=pagination)
            json_users = []
            for u in users:
                json_user = jsonable_encoder(u)
                json_users.append(json_user)
            return json_users
        case UserRole.USER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden operation for regular users.",
            )
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error",
            )


@router.get(
    path="/{user_id}",
    response_model=dto.UserResponse,
    responses={
        200: {"description": "Информация о мероприятии."},
        404: {"description": "Мероприятие с таким ID не найдено."},
    },
)
async def get_one(
    user_id: Annotated[int, Gt(0)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
):
    role = await get_user_role(auth_service, auth_claims.get("user_id", None))
    match role:
        case UserRole.ADMIN | UserRole.USER:
            user = await user_service.get_by_id(
                user_id=user_id,
            )
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error",
            )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No user with such id",
        )

    json_user = jsonable_encoder(user)
    return json_user


@router.post(
    path="",
    status_code=201,
    responses={
        201: {"description": "Пользователь создан успешно."},
        403: {"description": "Недостаточно прав для действия."},
    },
)
async def add_one(
    response: Response,
    user_service: Annotated[UserService, Depends(get_user_service)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
    data: Annotated[dto.UserCreateRequest, Body()],
):
    role = await get_user_role(auth_service, auth_claims.get("user_id", None))
    match role:
        case UserRole.ADMIN:
            match await user_service.add_one(data):
                case user_id, UserCreateStatus.OK:
                    response.headers["Location"] = f"/users/{user_id}"
                    return {"user_id": user_id}
                case None, UserCreateStatus.INSTITUTION_NOT_FOUND:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
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
                detail="Forbidden operation for regular users.",
            )
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error",
            )


@router.put(
    path="",
    responses={
        200: {"description": "Пользователь обновлен успешно."},
        403: {"description": "Недостаточно прав для выполнения действия."},
        404: {"description": "Пользователь или институт не найдены."},
        409: {"description": "При обновлении произошел конфликт версий."},
    },
)
async def update_one(
    response: Response,
    user_service: Annotated[UserService, Depends(get_user_service)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
    data: Annotated[dto.UserUpdateRequest, Body()],
):
    _ = await get_user_role(auth_service, auth_claims.get("user_id", None))
    match await user_service.update_one(data):
        case UserUpdateStatus.USER_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No user with such id",
            )
        case UserUpdateStatus.INSTITUTION_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No institution with such id",
            )
        case UserUpdateStatus.CONFLICT:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="The resource was updated by a third-party. Try re-fetching the data and repeat the operation.",
            )
        case UserUpdateStatus.OK:
            response.headers["Location"] = f"/users/{data.id}"
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error",
            )


@router.delete(
    path="/{user_id}",
    responses={
        200: {"description": "Пользователь удален успешно."},
        403: {"description": "Недостаточно прав для выполнения действия."},
    },
)
async def delete_one(
    user_id: Annotated[int, Gt(0)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
):
    role = await get_user_role(auth_service, auth_claims.get("user_id", None))
    match role:
        case UserRole.ADMIN:
            match await user_service.delete_one(user_id=user_id):
                case UserDeleteStatus.NOT_FOUND:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="No user with such id",
                    )
                case UserDeleteStatus.OK:
                    pass
                case _:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Unexpected error",
                    )
        case UserRole.USER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden operation for regular users.",
            )
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error",
            )
