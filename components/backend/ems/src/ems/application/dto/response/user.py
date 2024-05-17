from typing import Optional

from ems.application.dto.response import InstitutionResponse
from ems.application.enum import UserRole
from pydantic import BaseModel, Field, RootModel


class UserResponse(BaseModel):
    id: int = Field(
        gt=0,
        description="Уникальный идентификатор",
    )
    last_name: str = Field(
        description="Фамилия",
    )
    first_name: str = Field(
        description="Имя",
    )
    middle_name: Optional[str] = Field(
        default=None,
        description="Отчество",
    )
    institution: Optional[InstitutionResponse] = Field(
        default=None,
        description="Институт (факультет)"
    )
    course: Optional[int] = Field(
        default=None, gt=0, description="Курс (только для студентов)"
    )
    group: Optional[int] = Field(
        default=None,
        gt=0,
        description="Номер учебной группы (только для студентов)",
    )
    role: UserRole = Field(description="Роль пользователя")
    version: int = Field(description="Версия записи в базе данных")


class UserListResponse(RootModel[list[UserResponse]]):
    root: list[UserResponse]
