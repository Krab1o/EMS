from .request import *
from .response import *

from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    page: int = Field(
        ge=0,
        description='Индекс страницы'
    )
    size: int = Field(
        ge=1,
        description='Размер каждой страницы'
    )
