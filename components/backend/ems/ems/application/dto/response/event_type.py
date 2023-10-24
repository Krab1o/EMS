from typing import Optional

from pydantic import BaseModel, Field


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
