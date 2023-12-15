from typing import Annotated, Any

from annotated_types import Gt
from fastapi import (
    APIRouter,
    Depends,
    Response,
    Body,
    HTTPException,
    status
)

from ems.adapters.http_api.auth import get_auth_payload
from ems.adapters.http_api.dependencies import get_event_type_service

from ems.application import dto
from ems.application.enum import UserRole, EventStatus
from ems.application.services import EventTypeService
from ems.application.services.event_type_service import (
    EventTypeCreateStatus,
    EventTypeUpdateStatus,
    EventTypeDeleteStatus,
)

router = APIRouter(
    prefix='/event-types',
    tags=['Типы мероприятий']
)

@router.get(
    path='',
    response_model=dto.EventTypeListResponse,
    responses={
        200: {'description': 'Список типов мероприятий.'},
    }
)
async def get_list(
        event_type_service: Annotated[EventTypeService, Depends(get_event_type_service)],
        auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
        pagination: Annotated[dto.PaginationParams, Depends()],
):
    role = auth_claims.get('role', None)
    match role:
        case UserRole.ADMIN | UserRole.USER:
            return await event_type_service.get_list(
                params=pagination,
            )
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Unexpected error',
            )


@router.get(
    path='/{event_id}',
    response_model=dto.EventTypeResponse,
    responses={
        200: {'description': 'Информация о типе мероприятия.'},
        404: {'description': 'Тип мероприятия с таким ID не найден.'},
    }
)
async def get_one(
        event_type_id: Annotated[int, Gt(0)],
        auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
        event_type_service: Annotated[EventTypeService, Depends(get_event_type_service)],
):
    role = auth_claims.get('role', None)
    match role:
        case UserRole.ADMIN | UserRole.USER:
            event = await event_type_service.get_by_id(
                event_type_id=event_type_id,
            )

            if event is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='No event type with such id',
                )
            return event
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Unexpected error',
            )


@router.post(
    path='',
    status_code=201,
    responses={
        201: {'description': 'Тип мероприятия создан успешно.'},
        404: {'description': 'Тип мероприятия не найден.'},
        403: {'description': 'Недостаточно прав для действия.'},
    }
)
async def add_one(
        response: Response,
        event_type_service: Annotated[EventTypeService, Depends(get_event_type_service)],
        auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
        event_type_data: Annotated[dto.EventTypeCreateRequest, Body()],
):
    role = auth_claims.get('role', None)
    match role:
        case UserRole.ADMIN:
            match await event_type_service.add_one(event_type_data):
                case event_id, EventTypeCreateStatus.OK:
                    response.headers['Location'] = f'/event-types/{event_id}'
                case _:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail='Unexpected error',
                    )
        case UserRole.USER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Forbidden operation for a regular user.'
            )
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Unexpected error'
            )


@router.put(
    path='',
    responses={
        200: {'description': 'Тип мероприятия обновлен успешно.'},
        403: {'description': 'Недостаточно прав для выполнения действия.'},
        404: {'description': 'Тип мероприятия не найден.'},
        409: {'description': 'При обновлении произошел конфликт версий.'},
    }
)
async def update_one(
        response: Response,
        event_type_service: Annotated[EventTypeService, Depends(get_event_type_service)],
        auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
        data: Annotated[dto.EventTypeUpdateRequest, Body()],
):
    role = auth_claims.get('role', None)
    match role:
        case UserRole.ADMIN:
            match await event_type_service.update_one(data):
                case EventTypeUpdateStatus.OK:
                    response.headers['Location'] = f'/event-types/{event_id}'
                case EventTypeUpdateStatus.NOT_FOUND:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail='No event type with such id',
                    )
                case EventTypeUpdateStatus.CONFLICT:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail='The resource was updated by a third-party. Try re-fetching the data and repeat the operation.'
                    )
                case _:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail='Unexpected error',
                    )
        case UserRole.USER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Forbidden operation for a regular user.'
            )
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Unexpected error'
            )


@router.delete(
    path='/{event_id}',
    responses={
        200: {'description': 'Тип мероприятия удален успешно.'},
        403: {'description': 'Недостаточно прав для выполнения действия.'},
    }
)
async def delete_one(
        event_type_id: Annotated[int, Gt(0)],
        event_type_service: Annotated[EventTypeService, Depends(get_event_type_service)],
        auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
):
    role = auth_claims.get('role', None)
    match role:
        case UserRole.ADMIN:
            match await event_type_service.delete_one(event_type_id):
                case EventTypeDeleteStatus.NOT_FOUND:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail='No event type with such id',
                    )
                case EventTypeDeleteStatus.OK:
                    pass
        case UserRole.USER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Forbidden operation for a regular user.'
            )
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Unexpected error'
            )

