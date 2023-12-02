from typing import Optional

from pydantic import BaseModel, Field, RootModel


class EventTypeResponse(BaseModel):
    id: int = Field(
        gt=0,
        description='Уникальный идентификатор',
    )
    title: str = Field(
        description='Название типа мероприятия'
    )
    description: Optional[str] = Field(
        default=None,
        description='Описание типа мероприятия'
    )
    version: int = Field(
        description='Версия записи в базе данных'
    )


class EventListResponse(RootModel[list[EventTypeResponse]]):
    root: list[EventTypeResponse]
