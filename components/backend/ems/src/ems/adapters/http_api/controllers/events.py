from datetime import datetime as dt
from typing import Annotated, Any

from annotated_types import Gt
from ems.adapters.http_api.auth import get_auth_payload, get_user_role
from ems.adapters.http_api.dependencies import (
    get_auth_service,
    get_event_service,
    get_user_service
)
from ems.application import dto
from ems.application.enum import EventStatus, UserRole
from ems.application.services import AuthService, EventService, UserService
from ems.application.services.event_service import (
    EventCreateStatus,
    EventDeleteStatus,
    EventUpdateStatus,
    EventVoteStatus,
)
from fastapi import (
    APIRouter,
    Body,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    Response,
    UploadFile,
    status,
)
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/events", tags=["Мероприятия"])


@router.get(
    path="",
    response_model=dto.EventListResponse,
    responses={
        200: {"description": "Список мероприятий."},
    },
)
async def get_list(
        event_service: Annotated[EventService, Depends(get_event_service)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
        pagination: Annotated[dto.PaginationParams, Depends()],
        event_type: Annotated[list[int], Query()] = None,
        event_status: Annotated[list[EventStatus], Query()] = None,
):
    user_id = auth_claims.get("user_id", None)
    role = await get_user_role(auth_service, user_id)
    match role:
        case UserRole.ADMIN:
            events = await event_service.get_list(
                params=pagination,
                user_id=user_id,
                status=event_status,
                event_type=event_type,
            )
        case UserRole.USER:
            events = await event_service.get_list(
                params=pagination,
                user_id=user_id,
                status=(
                    [
                        s
                        for s in event_status
                        if s
                           not in (EventStatus.REJECTED, EventStatus.ON_REVIEW)
                    ]
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
                detail="Unexpected error",
            )

    json_events = []
    for e in events:
        json_event = jsonable_encoder(e)
        if e.cover_id is not None:
            json_event["cover"]["uri"] = f"/covers/{e.cover_id}"
        json_events.append(json_event)
    return json_events


@router.get(
    path="/{event_id}",
    response_model=dto.EventResponse,
    responses={
        200: {"description": "Информация о мероприятии."},
        404: {"description": "Мероприятие с таким ID не найдено."},
    },
)
async def get_one(
        event_id: Annotated[int, Gt(0)],
        event_service: Annotated[EventService, Depends(get_event_service)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
):
    user_id = auth_claims.get("user_id", None)
    role = await get_user_role(auth_service, user_id)
    match role:
        case UserRole.ADMIN:
            event = await event_service.get_by_id(
                event_id=event_id,
                user_id=user_id,
                include_rejected=True,
                include_on_review=True,
            )
        case UserRole.USER:
            event = await event_service.get_by_id(
                event_id=event_id,
                user_id=user_id,
                include_rejected=False,
            )
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error",
            )

    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No event with such id",
        )

    json_event = jsonable_encoder(event)
    if event.cover_id is not None:
        json_event["cover"]["uri"] = f"/covers/{event.cover_id}"
    return json_event


@router.post(
    path="",
    status_code=201,
    responses={
        201: {"description": "Мероприятие создано успешно."},
        404: {"description": "Тип мероприятия или обложка не найдены."},
        403: {"description": "Недостаточно прав для действия."},
        409: {
            "description": "Слишком много событий находятся еще на рассмотрении."
        },
    },
)
async def add_one(
        response: Response,
        event_service: Annotated[EventService, Depends(get_event_service)],
        auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
        title: Annotated[str, Form()],
        place_id: Annotated[int, Form()],
        datetime: Annotated[dt, Form()],
        dateend: Annotated[dt, Form()],
        type_id: Annotated[int, Gt(0), Form()],
        description: Annotated[str, Form()] = None,
        cover: Annotated[UploadFile, File()] = None,
):
    # спасибо FastAPI, очень удобно сделали!
    event_data = dto.EventCreateRequest(
        title=title,
        place_id=place_id,
        datetime=datetime,
        dateend=dateend,
        type_id=type_id,
        description=description,
    )
    match await event_service.add_one(
        event_data, creator_id=auth_claims.get("user_id"), cover=cover
    ):
        case None, EventCreateStatus.EVENT_TYPE_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No event type with such id",
            )
        case None, EventCreateStatus.EVENT_TYPE_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No cover with such id",
            )
        case None, EventCreateStatus.TOO_MANY_OPENED_EVENTS:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Too many events still on review",
            )
        case None, EventCreateStatus.UNEXPECTED_ERROR:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred when tried to insert a new record",
            )
        case event_id, EventCreateStatus.OK:
            response.headers["Location"] = f"/events/{event_id}"
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error",
            )


@router.post(
    path="/check_date",
    status_code=201,
    responses={
        201: {"description": "Мероприятие создано успешно."},
        404: {"description": "Тип мероприятия или обложка не найдены."},
        403: {"description": "Недостаточно прав для действия."},
        409: {
            "description": "Слишком много событий находятся еще на рассмотрении."
        },
    },
)
async def check(
        event_service: Annotated[EventService, Depends(get_event_service)],
        user_service: Annotated[UserService, Depends(get_user_service)],
        pagination: Annotated[dto.PaginationParams, Depends()],
        datestart: dt,
        dateend: dt,
        place_id: int

):
    users = await user_service.get_list(params=pagination)
    for user in users:
        events = await event_service.get_list(
            params=pagination,
            user_id=user.id,
            place_id=[place_id])
        for event in events:
            if event.datetime < datestart < event.dateend or event.datetime < dateend < event.dateend:
                return False
    return True

@router.put(
    path="",
    responses={
        200: {"description": "Мероприятие обновлено успешно."},
        400: {"description": "Место проведения или обложка не найдены."},
        403: {"description": "Недостаточно прав для выполнения действия."},
        404: {"description": "Мероприятие с таким ID не найдено."},
    },
)
async def update_one(
        response: Response,
        event_service: Annotated[EventService, Depends(get_event_service)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
        data: Annotated[dto.EventUpdateRequest, Body()],
):
    # TODO: обновление обложки
    user_id = auth_claims.get("user_id", None)
    role = await get_user_role(auth_service, user_id)
    match await event_service.update_one(
        data, user_id=user_id, user_role=role
    ):
        case EventUpdateStatus.EVENT_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No event with such id",
            )
        case EventUpdateStatus.COVER_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_400_NOT_FOUND,
                detail="No cover with such id",
            )
        case EventUpdateStatus.PLACE_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_400_NOT_FOUND,
                detail="No place with such id",
            )
        case EventUpdateStatus.FORBIDDEN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Regular users are only able to update their own events. Administrators may update any.",
            )
        case EventUpdateStatus.OK:
            response.headers["Location"] = f"/events/{data.id}"
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error",
            )


@router.delete(
    path="/{event_id}",
    responses={
        200: {"description": "Мероприятие удалено успешно."},
        403: {"description": "Недостаточно прав для выполнения действия."},
    },
)
async def delete_one(
        event_id: Annotated[int, Gt(0)],
        event_service: Annotated[EventService, Depends(get_event_service)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
):
    user_id = auth_claims.get("user_id", None)
    role = await get_user_role(auth_service, user_id)
    match await event_service.delete_one(
        event_id=event_id, user_id=user_id, user_role=role
    ):
        case EventDeleteStatus.NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No event with such id",
            )
        case EventDeleteStatus.FORBIDDEN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Regular users are only able to update their own events. Administrators may update any.",
            )
        case EventDeleteStatus.OK:
            pass
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error",
            )


@router.post(
    path="/{event_id}/vote",
    responses={
        200: {"description": "Голос записан."},
        404: {"description": "Мероприятие или пользователь не найден."},
        409: {"description": "Мероприятие не на стадии голосования."},
    },
)
async def vote(
        event_id: Annotated[int, Gt(0)],
        event_service: Annotated[EventService, Depends(get_event_service)],
        auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
        vote_data: Annotated[dto.EventVoteRequest, Body()],
):
    user_id = auth_claims.get("user_id", None)
    match await event_service.vote(
        data=vote_data, event_id=event_id, user_id=user_id
    ):
        case EventVoteStatus.EVENT_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No event with such id",
            )
        case EventVoteStatus.USER_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No user with such id",
            )
        case EventVoteStatus.NOT_ON_POLL:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This event is not on poll",
            )
        case EventVoteStatus.OK:
            pass
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error",
            )
