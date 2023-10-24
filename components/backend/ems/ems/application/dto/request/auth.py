from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str = Field(
        description='E-mail, указанный при регистрации'
    )
    password: str = Field(
        description='Пароль пользователя'
    )
