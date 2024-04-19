from typing import Optional

from ems.application.dto.response.institution import InstitutionResponse
from pydantic import BaseModel, Field, RootModel


class PlaceResponse(BaseModel):
    id: int = Field(gt=0)
    title: str
    floor: Optional[int] = Field(default=None, gt=0)
    institution_id: Optional[int] = Field(default=None)
    institution: Optional[InstitutionResponse] = Field(default=None)


class PlaceListResponse(RootModel):
    root: list[PlaceResponse]
