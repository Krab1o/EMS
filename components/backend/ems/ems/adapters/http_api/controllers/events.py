from typing import Annotated, Any

from annotated_types import Gt
from fastapi import (
    APIRouter,
    Depends,
    Response,
    Body,
    HTTPException,
    status,
)

from ems.adapters.http_api.auth import get_auth_payload
from ems.adapters.http_api.dependencies import get_event_service

from ems.application import dto
from ems.application.enum import UserRole
from ems.application.services import EventService
from ems.application.services.event_service import EventCreateStatus

router = APIRouter(
    prefix='/events',
    tags=['Мероприятия']
)


@router.get(
    path='',
    response_model=dto.EventListResponse,
    responses={
        200: {'description': 'Список мероприятий.'},
        403: {'description': 'Недостаточно прав для действия.'}
    }
)
async def get_list(
        event_service: Annotated[EventService, Depends(get_event_service)],
        auth_claims: dict[str, Any] = Depends(get_auth_payload),
        pagination: dto.PaginationParams = Depends(),
):
    role = auth_claims.get('role', None)
    if role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail='Insufficient privileges for the action',
        )

    return await event_service.get_list(pagination)


@router.get(
    path='/{event_id}',
    response_model=dto.EventResponse,
    responses={
        200: {'description': 'Информация о мероприятии.'},
        403: {'description': 'Недостаточно прав для действия.'},
        404: {'description': 'Мероприятие с таким ID не найдено.'},
    }
)
async def get_one(
        event_id: Annotated[int, Gt(0)],
        event_service: Annotated[EventService, Depends(get_event_service)],
        auth_claims: dict[str, Any] = Depends(get_auth_payload)
):
    role = auth_claims.get('role', None)
    if role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Insufficient privileges for the action',
        )

    event = await event_service.get_one(event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No event with such id',
        )
    return event


@router.post(
    path='',
    status_code=201,
    responses={
        201: {'description': 'Мероприятие создано успешно.'},
        400: {'description': 'Тип события не найден.'},
    }
)
async def add_one(
        response: Response,
        event_service: Annotated[EventService, Depends(get_event_service)],
        auth_claims: dict[str, Any] = Depends(get_auth_payload),
        event_data: dto.EventCreateRequest = Body(),
):
    role = auth_claims.get('role', None)
    if role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Insufficient rights for the action',
        )

    match await event_service.add_one(auth_claims.get('user_id'), event_data):
        case None, EventCreateStatus.EVENT_TYPE_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='No event type with such id',
            )
        case None, EventCreateStatus.UNEXPECTED_ERROR:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='An error occurred when tried to insert a new record'
            )
        case event_id, EventCreateStatus.OK:
            response.headers['Location'] = f'/events/{event_id}'
