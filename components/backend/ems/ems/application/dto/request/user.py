from typing import Optional

from pydantic import Field, BaseModel


class UserCreateRequest(BaseModel):
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
    institution_id: int = Field(
        gt=0,
        description='Идентификатор института (факультета)',
    )
    course: int = Field(
        gt=0,
        description='Курс',
    )
    group: int = Field(
        gt=0,
        description='Номер учебной группы',
    )
    telegram: Optional[str] = Field(
        default=None,
        description='Имя пользователя Telegram',
    )
    vk: Optional[str] = Field(
        default=None,
        description='ID ВКонтакте',
    )
    phone_number: Optional[str] = Field(
        default=None,
        description='Номер телефона',
    )
    email: str = Field(
        description='E-mail'
    )
    password: str = Field(
        description='Пароль'
    )
