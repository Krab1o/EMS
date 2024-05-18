from pydantic import BaseModel, Field

from .auth import LoginRequest
from .user import UserCreateRequest, UserUpdateRequest, UserTelegramCredentialsUpdateRequest
from .event import EventCreateRequest, EventUpdateRequest, EventVoteRequest
from .event_type import EventTypeCreateRequest, EventTypeUpdateRequest
from .club import ClubCreateRequest, ClubUpdateRequest, ClubFavoriteRequest
from .place import PlaceCreateRequest, PlaceUpdateRequest


class PaginationParams(BaseModel):
    page: int = Field(
        ge=0,
        default=0,
        description='Индекс страницы'
    )
    size: int = Field(
        ge=1,
        lt=51,
        default=20,
        description='Размер каждой страницы'
    )
