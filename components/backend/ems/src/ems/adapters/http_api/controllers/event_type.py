from typing import Annotated, Any

from annotated_types import Gt
from ems.adapters.http_api.auth import get_auth_payload, get_user_role
from ems.adapters.http_api.dependencies import (
    get_auth_service,
    get_event_type_service,
)
from ems.application import dto
from ems.application.enum import UserRole
from ems.application.services import AuthService, EventTypeService
from ems.application.services.event_type_service import (
    EventTypeCreateStatus,
    EventTypeDeleteStatus,
    EventTypeUpdateStatus,
)
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status

router = APIRouter(prefix="/event-types", tags=["Типы мероприятий"])


@router.get(
    path="",
    response_model=dto.EventTypeListResponse,
    responses={
        200: {"description": "Список типов мероприятий."},
    },
)
async def get_list(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    event_type_service: Annotated[
        EventTypeService, Depends(get_event_type_service)
    ],
    auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
    pagination: Annotated[dto.PaginationParams, Depends()],
):
    role = await get_user_role(auth_service, auth_claims.get("user_id", None))
    match role:
        case UserRole.ADMIN | UserRole.USER:
            return await event_type_service.get_list(
                params=pagination,
            )
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error",
            )


@router.get(
    path="/{event_type_id}",
    response_model=dto.EventTypeResponse,
    responses={
        200: {"description": "Информация о типе мероприятия."},
        404: {"description": "Тип мероприятия с таким ID не найден."},
    },
)
async def get_one(
    event_type_id: Annotated[int, Gt(0)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
    event_type_service: Annotated[
        EventTypeService, Depends(get_event_type_service)
    ],
):
    role = await get_user_role(auth_service, auth_claims.get("user_id", None))
    match role:
        case UserRole.ADMIN | UserRole.USER:
            event = await event_type_service.get_by_id(
                event_type_id=event_type_id,
            )

            if event is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No event type with such id",
                )
            return event
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error",
            )


@router.post(
    path="",
    status_code=201,
    responses={
        201: {"description": "Тип мероприятия создан успешно."},
        404: {"description": "Тип мероприятия не найден."},
        403: {"description": "Недостаточно прав для действия."},
    },
)
async def add_one(
    response: Response,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    event_type_service: Annotated[
        EventTypeService, Depends(get_event_type_service)
    ],
    auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
    event_type_data: Annotated[dto.EventTypeCreateRequest, Body()],
):
    role = await get_user_role(auth_service, auth_claims.get("user_id", None))
    match role:
        case UserRole.ADMIN:
            match await event_type_service.add_one(event_type_data):
                case event_id, EventTypeCreateStatus.OK:
                    response.headers["Location"] = f"/event-types/{event_id}"
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
        200: {"description": "Тип мероприятия обновлен успешно."},
        403: {"description": "Недостаточно прав для выполнения действия."},
        404: {"description": "Тип мероприятия не найден."},
        409: {"description": "При обновлении произошел конфликт версий."},
    },
)
async def update_one(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    event_type_service: Annotated[
        EventTypeService, Depends(get_event_type_service)
    ],
    auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
    data: Annotated[dto.EventTypeUpdateRequest, Body()],
):
    role = await get_user_role(auth_service, auth_claims.get("user_id", None))
    match role:
        case UserRole.ADMIN:
            match await event_type_service.update_one(data):
                case EventTypeUpdateStatus.OK:
                    pass
                case EventTypeUpdateStatus.NOT_FOUND:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="No event type with such id",
                    )
                case EventTypeUpdateStatus.CONFLICT:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="The resource was updated by a third-party. Try re-fetching the data and repeat the operation.",
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
    path="/{event_id}",
    responses={
        200: {"description": "Тип мероприятия удален успешно."},
        403: {"description": "Недостаточно прав для выполнения действия."},
    },
)
async def delete_one(
    event_type_id: Annotated[int, Gt(0)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    event_type_service: Annotated[
        EventTypeService, Depends(get_event_type_service)
    ],
    auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
):
    role = await get_user_role(auth_service, auth_claims.get("user_id", None))
    match role:
        case UserRole.ADMIN:
            match await event_type_service.delete_one(event_type_id):
                case EventTypeDeleteStatus.NOT_FOUND:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="No event type with such id",
                    )
                case EventTypeDeleteStatus.OK:
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
