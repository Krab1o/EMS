from typing import Annotated, Any

from annotated_types import Gt
from fastapi import APIRouter, Depends, Response, Body

from ems.adapters.http_api.auth import get_auth_payload
from ems.adapters.http_api.dependencies import get_event_service

from ems.application import dto
from ems.application.enum import UserRole
from ems.application.services import EventService


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
        response: Response,
        event_service: Annotated[EventService, Depends(get_event_service)],
        auth_claims: dict[str, Any] = Depends(get_auth_payload),
        pagination: dto.PaginationParams = Depends(),
):
    role = auth_claims.get('role', None)
    if role != UserRole.ADMIN:
        response.status_code = 403
        return response

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
        response: Response,
        event_id: Annotated[int, Gt(0)],
        event_service: Annotated[EventService, Depends(get_event_service)],
        auth_claims: dict[str, Any] = Depends(get_auth_payload)
):
    role = auth_claims.get('role', None)
    if role != UserRole.ADMIN:
        response.status_code = 403
        return response

    event = await event_service.get_one(event_id)
    if event is None:
        response.status_code = 404
        return response
    return event


@router.post(
    path='/{event_id}',
    status_code=201,
    response_model=dto.EventResponse,
    responses={
        201: {'description': 'Информация о вновь созданном мероприятии.'},
        400: {'description': 'Формат некоторых полей неверный или тип события не найден.'}
    }
)
async def add_one(
        response: Response,
        event_service: Annotated[EventService, Depends(get_event_service)],
        auth_claims: dict[str, Any] = Depends(get_auth_payload),
        event_data: dto.EventCreateRequest = Body(),
):
    pass
