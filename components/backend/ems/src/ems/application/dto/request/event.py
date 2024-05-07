from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel, Field


class EventCreateRequest(BaseModel):
    title: str = Field(
        min_length=3,
        description="Название",
    )
    description: Optional[str] = Field(
        default=None,
        min_length=1,
        description="Описание мероприятия",
    )
    place_id: int = Field(
        description="Идентификатор места проведения",
    )
    datetime: dt = Field(
        description="Дата и время начала мероприятия",
    )
    dateend: dt = Field(
        description="Дата и время конца мероприятия",
    )
    type_id: int = Field(
        gt=0,
        description="Идентификатор типа мероприятия",
    )


class EventUpdateRequest(BaseModel):
    id: int = Field(
        gt=0,
        description="Уникальный идентификатор",
    )
    title: str = Field(
        min_length=3,
        description="Название",
    )
    description: Optional[str] = Field(
        default=None,
        min_length=1,
        description="Описание мероприятия",
    )
    status: Optional[str] = Field(
        default=None,
        description="(Для администратора) Новый статус мероприятия",
    )
    cover_id: Optional[int] = Field(
        default=None,
        description="Идентификатор обложки мероприятия",
    )
    place_id: int = Field(
        description="Идентификатор места проведения",
    )
    datetime: dt = Field(
        description="Дата и время начала мероприятия",
    )
    dateend: dt = Field(
        description="Дата и время конца мероприятия",
    )


class EventVoteRequest(BaseModel):
    like: bool = Field(description="Голос (да/нет)")
