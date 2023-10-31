from pydantic import BaseModel, Field

from .auth import LoginRequest
from .user import UserCreateRequest
from .event import EventCreateRequest


class PaginationParams(BaseModel):
    page: int = Field(
        ge=0,
        description='Индекс страницы'
    )
    size: int = Field(
        ge=1,
        lt=51,
        description='Размер каждой страницы'
    )
