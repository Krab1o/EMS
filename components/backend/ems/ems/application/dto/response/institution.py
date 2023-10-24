from typing import Optional

from pydantic import BaseModel, Field


class InstitutionResponse(BaseModel):
    id: int = Field(
        gt=0,
        description='Уникальный идентификатор'
    )
    title: str = Field(
        description='Название института (факультета)'
    )
    description: Optional[str] = Field(
        default=None,
        description='Описание института (факультета)'
    )
