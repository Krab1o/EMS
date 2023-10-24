from typing import Optional

from pydantic import BaseModel, Field, RootModel

from ems.application.dto.response import InstitutionResponse
from ems.application.enum import UserRole


class UserListElement(BaseModel):
    id: int = Field(
        gt=0,
        description='Уникальный идентификатор',
    )
    last_name: str = Field(
        description='Фамилия',
    )
    first_name: str = Field(
        description='Имя',
    )
    middle_name: Optional[str] = Field(
        default=None,
        description='Отчество',
    )
    institution: InstitutionResponse = Field(
        description='Институт (факультет)'
    )
    course: Optional[int] = Field(
        default=None,
        gt=0,
        description='Курс (только для студентов)'
    )
    group: Optional[int] = Field(
        default=None,
        gt=0,
        description='Номер учебной группы (только для студентов)'
    )
    role: UserRole = Field(
        description='Роль пользователя'
    )


class UserListResponse(RootModel[list[UserListElement]]):
    root: list[UserListElement]
