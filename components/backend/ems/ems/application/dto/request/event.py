from typing import Optional
from datetime import datetime as dt

from pydantic import BaseModel, Field


class EventCreateRequest(BaseModel):
    title: str = Field(
        min_length=3,
        description='Название',
    )
    description: Optional[str] = Field(
        default=None,
        min_length=1,
        description='Описание мероприятия',
    )
    cover_id: Optional[int] = Field(
        default=None,
        description='Идентификатор обложки мероприятия',
    )
    place: str = Field(
        description='Место проведения',
    )
    datetime: dt = Field(
        description='Дата и время проведения',
    )
    type_id: int = Field(
        gt=0,
        description='Идентификатор типа мероприятия',
    )


class EventUpdateRequest(BaseModel):
    id: int = Field(
        gt=0,
        description='Уникальный идентификатор',
    )
    title: str = Field(
        min_length=3,
        description='Название',
    )
    description: Optional[str] = Field(
        default=None,
        min_length=1,
        description='Описание мероприятия',
    )
    cover_id: Optional[int] = Field(
        default=None,
        description='Идентификатор обложки мероприятия',
    )
    place: str = Field(
        description='Место проведения',
    )
    datetime: dt = Field(
        description='Дата и время проведения',
    )
    version: int = Field(
        ge=0,
        description='Версия обновленной записи (на 1 больше предыдущей версии)'
    )


class EventVoteRequest(BaseModel):
    like: bool = Field(
        description='Голос (да/нет)'
    )
