from typing import Annotated, Any

from annotated_types import Gt
from fastapi import (
    APIRouter,
    Depends,
    Response,
    Body,
    HTTPException,
    status,
    Query,
)

from ems.adapters.http_api.auth import get_auth_payload
from ems.adapters.http_api.dependencies import get_event_service

from ems.application import dto
from ems.application.enum import UserRole, EventStatus
from ems.application.services import EventService
from ems.application.services.event_service import EventCreateStatus, EventUpdateStatus, EventDeleteStatus, \
    EventVoteStatus

router = APIRouter(
    prefix='/events',
    tags=['Мероприятия']
)


@router.get(
    path='',
    response_model=dto.EventListResponse,
    responses={
        200: {'description': 'Список мероприятий.'},
    }
)
async def get_list(
        event_service: Annotated[EventService, Depends(get_event_service)],
        auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
        pagination: Annotated[dto.PaginationParams, Depends()],
        event_type: Annotated[list[int], Query()] = None,
        event_status: Annotated[list[EventStatus], Query()] = None,
):
    role = auth_claims.get('role', None)
    match role:
        case UserRole.ADMIN:
            return await event_service.get_list(
                pagination,
                status=event_status,
                event_type=event_type,
            )
        case UserRole.USER:
            return await event_service.get_list(
                pagination,
                status=(
                    [s for s in event_status if s not in (EventStatus.REJECTED, EventStatus.ON_REVIEW)]
                    if event_status is not None
                    else [
                        EventStatus.ON_POLL,
                        EventStatus.PLANNED,
                        EventStatus.ENDED,
                        EventStatus.CANCELLED,
                    ]
                ),
                event_type=event_type,
            )
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Unexpected error',
            )


@router.get(
    path='/{event_id}',
    response_model=dto.EventResponse,
    responses={
        200: {'description': 'Информация о мероприятии.'},
        404: {'description': 'Мероприятие с таким ID не найдено.'},
    }
)
async def get_one(
        event_id: Annotated[int, Gt(0)],
        event_service: Annotated[EventService, Depends(get_event_service)],
        auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
):
    role = auth_claims.get('role', None)
    match role:
        case UserRole.ADMIN:
            event = await event_service.get_by_id(event_id, include_rejected=True)
        case UserRole.USER:
            event = await event_service.get_by_id(event_id, include_rejected=False)
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Unexpected error',
            )

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
        403: {'description': 'Недостаточно прав для действия.'},
    }
)
async def add_one(
        response: Response,
        event_service: Annotated[EventService, Depends(get_event_service)],
        auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
        event_data: Annotated[dto.EventCreateRequest, Body()],
):
    match await event_service.add_one(event_data, creator_id=auth_claims.get('user_id')):
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
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Unexpected error',
            )


@router.put(
    path='',
    responses={
        200: {'description': 'Мероприятие обновлено успешно.'},
        403: {'description': 'Недостаточно прав для выполнения действия.'},
        409: {'description': 'При обновлении произошел конфликт версий.'},
    }
)
async def update_one(
        response: Response,
        event_service: Annotated[EventService, Depends(get_event_service)],
        auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
        data: Annotated[dto.EventUpdateRequest, Body()],
):
    role = auth_claims.get('role', None)
    user_id = auth_claims.get('user_id', None)
    match await event_service.update_one(data, user_id=user_id, user_role=role):
        case EventUpdateStatus.NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No event with such id',
            )
        case EventUpdateStatus.FORBIDDEN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Regular users are only able to update their own events. Administrators may update any.'
            )
        case EventUpdateStatus.CONFLICT:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='The resource was updated by a third-party. Try re-fetching the data and repeat the operation.'
            )
        case EventUpdateStatus.OK:
            response.headers['Location'] = f'/events/{data.id}'
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Unexpected error'
            )


@router.delete(
    path='/{event_id}',
    responses={
        200: {'description': 'Мероприятие удалено успешно.'},
        403: {'description': 'Недостаточно прав для выполнения действия.'},
    }
)
async def delete_one(
        event_id: Annotated[int, Gt(0)],
        event_service: Annotated[EventService, Depends(get_event_service)],
        auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
):
    role = auth_claims.get('role', None)
    user_id = auth_claims.get('user_id', None)
    match await event_service.delete_one(event_id=event_id, user_id=user_id, user_role=role):
        case EventDeleteStatus.NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No event with such id',
            )
        case EventDeleteStatus.FORBIDDEN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Regular users are only able to update their own events. Administrators may update any.'
            )
        case EventDeleteStatus.OK:
            pass
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Unexpected error'
            )


@router.post(
    path='/{event_id}/vote',
    responses={
        200: {'description': 'Голос записан.'},
        404: {'description': 'Мероприятие или пользователь не найден.'},
    }
)
async def vote(
        event_id: Annotated[int, Gt(0)],
        event_service: Annotated[EventService, Depends(get_event_service)],
        auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
        vote_data: Annotated[dto.EventVoteRequest, Body()],
):
    user_id = auth_claims.get('user_id', None)
    match await event_service.vote(data=vote_data, event_id=event_id, user_id=user_id):
        case EventVoteStatus.EVENT_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No event with such id',
            )
        case EventVoteStatus.USER_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No user with such id',
            )
        case EventVoteStatus.NOT_ON_POLL:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='This event is not on poll',
            )
        case EventVoteStatus.OK:
            pass
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Unexpected error'
            )
