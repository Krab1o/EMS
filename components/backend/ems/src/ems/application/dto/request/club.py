from typing import Optional

from pydantic import BaseModel, Field


class ClubCreateRequest(BaseModel):
    title: str = Field(description="Название")
    description: str = Field(description="Описание")
    telegram: Optional[str] = Field(default=None, description="Telegram")
    vk: Optional[str] = Field(default=None, description="VK")
    youtube: Optional[str] = Field(default=None, description="YouTube")
    rutube: Optional[str] = Field(default=None, description="Rutube")
    tiktok: Optional[str] = Field(default=None, description="TikTok")


class ClubUpdateRequest(BaseModel):
    title: str = Field(description="Название")
    description: str = Field(description="Описание")
    telegram: Optional[str] = Field(default=None, description="Telegram")
    vk: Optional[str] = Field(default=None, description="VK")
    youtube: Optional[str] = Field(default=None, description="YouTube")
    rutube: Optional[str] = Field(default=None, description="Rutube")
    tiktok: Optional[str] = Field(default=None, description="TikTok")


class ClubFavoriteRequest(BaseModel):
    is_favorite: bool = Field(description="Избранное")
