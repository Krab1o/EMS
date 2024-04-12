from typing import Optional

from ems.application.dto.response.user import UserResponse
from pydantic import BaseModel, Field, RootModel


class ClubListElement(BaseModel):
    id: int = Field(gt=0, description="Уникальный идентификатор")
    title: str = Field(description="Название")
    description: str = Field(description="Описание")
    telegram: Optional[str] = Field(default=None, description="Telegram")
    vk: Optional[str] = Field(default=None, description="VK")
    youtube: Optional[str] = Field(default=None, description="YouTube")
    rutube: Optional[str] = Field(default=None, description="Rutube")
    tiktok: Optional[str] = Field(default=None, description="TikTok")
    is_favorite: bool = Field(
        default=False,
    )


class ClubListResponse(RootModel[list[ClubListElement]]):
    root: list[ClubListElement]


class ClubResponse(BaseModel):
    id: int = Field(gt=0, description="Уникальный идентификатор")
    title: str = Field(description="Название")
    description: str = Field(description="Описание")
    telegram: Optional[str] = Field(default=None, description="Telegram")
    vk: Optional[str] = Field(default=None, description="VK")
    youtube: Optional[str] = Field(default=None, description="YouTube")
    rutube: Optional[str] = Field(default=None, description="Rutube")
    tiktok: Optional[str] = Field(default=None, description="TikTok")
    users_favorite: list[UserResponse] = Field(default=list)
    is_favorite: bool = Field(
        default=False,
    )
