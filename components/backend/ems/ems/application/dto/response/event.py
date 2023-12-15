from typing import Optional
from pydantic import BaseModel, Field, RootModel
from datetime import datetime as dt

from ems.application.dto.response import (
    UserResponse,
    EventTypeResponse,
    CoverResponse,
)


class EventListElement(BaseModel):
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
    cover_id: Optional[int] = Field(
        default=None,
        description='Идентификатор обложки мероприятия'
    )
    cover: Optional[CoverResponse] = Field(
        default=None,
        description='Обложка мероприятия'
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
    user_vote: Optional[bool] = Field(
        default=None,
        description='Оценка, которую текущий пользователь поставил мероприятию'
    )
    version: int = Field(
        description='Версия записи в базе данных'
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
    cover: Optional[CoverResponse] = Field(
        default=None,
        description='Обложка мероприятия'
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
    creator: UserResponse = Field(
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
    users_voted: list[UserResponse] = Field(
        default_factory=list,
        description='Люди, голосовавшие за мероприятие'
    )
    user_vote: Optional[bool] = Field(
        default=None,
        description='Оценка, которую текущий пользователь поставил мероприятию'
    )
    version: int = Field(
        description='Версия записи в базе данных'
    )
