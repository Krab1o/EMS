from typing import Optional
from pydantic import BaseModel, Field, RootModel
from datetime import datetime as dt

from ems.application.dto.response import (
    UserListElement,
    EventTypeResponse,
)


class EventListElement(BaseModel):
    id: int = Field(
        gt=0,
        description='Уникальный идентификатор'
    )
    title: str = Field(
        description='Название'
    )
    cover: Optional[str] = Field(
        default=None,
        description='URI обложки мероприятия'
    )
    status: str = Field(
        description='Статус'
    )
    place: str = Field(
        description='Место проведения'
    )
    datetime: dt = Field(
        description='Дата и время проведения'
    )
    voted_yes: int = Field(
        ge=0,
        description='Количество пользователей, проголосовавших ЗА'
    )
    voted_no: int = Field(
        ge=0,
        description='Количество пользователей, проголосовавших ПРОТИВ'
    )


class EventListResponse(RootModel[list[EventListElement]]):
    root: list[EventListElement]


class EventResponse(BaseModel):
    id: int = Field(
        gt=0,
        description='Уникальный идентификатор'
    )
    title: str = Field(
        description='Название'
    )
    description: Optional[str] = Field(
        default=None,
        description='Описание'
    )
    cover: Optional[str] = Field(
        default=None,
        description='URI обложки мероприятия'
    )
    status: str = Field(
        description='Статус'
    )
    place: str = Field(
        description='Место проведения'
    )
    datetime: dt = Field(
        description='Дата и время проведения'
    )
    creator: UserListElement = Field(
        description='Информация о пользователе, создавшем мероприятие'
    )
    voted_yes: int = Field(
        ge=0,
        description='Количество пользователей, проголосовавших ЗА'
    )
    voted_no: int = Field(
        ge=0,
        description='Количество пользователей, проголосовавших ПРОТИВ'
    )
    type: EventTypeResponse = Field(
        description='Тип мероприятия'
    )
