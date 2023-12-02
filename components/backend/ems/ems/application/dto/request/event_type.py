from typing import Optional

from pydantic import BaseModel, Field


class EventTypeCreateRequest(BaseModel):
    title: str = Field(
        min_length=3,
        description='Имя типа мероприятия',
    )
    description: Optional[str] = Field(
        default=None,
        min_length=1,
        description='Описание типа мероприятия',
    )


class EventTypeUpdateRequest(BaseModel):
    id: int = Field(
        gt=0,
        description='Уникальный идентификатор',
    )
    title: str = Field(
        min_length=3,
        description='Имя типа мероприятия',
    )
    description: Optional[str] = Field(
        default=None,
        min_length=1,
        description='Описание типа мероприятия',
    )
    version: int = Field(
        ge=0,
        description='Версия обновленной записи (на 1 больше предыдущей версии)'
    )
