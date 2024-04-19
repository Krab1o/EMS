from typing import Optional

from pydantic import BaseModel, Field


class PlaceCreateRequest(BaseModel):
    title: str
    floor: Optional[int] = Field(default=None, gt=0)
    institution_id: Optional[int] = Field(default=None)


class PlaceUpdateRequest(BaseModel):
    id: int = Field(gt=0)
    title: str
    floor: Optional[int] = Field(default=None, gt=0)
    institution_id: Optional[int] = Field(default=None)
