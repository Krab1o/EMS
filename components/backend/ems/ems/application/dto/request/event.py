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
    cover: Optional[str] = Field(
        description='URI обложки мероприятия',
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
