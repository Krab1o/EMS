from typing import Optional

from pydantic import BaseModel, Field


class CoverResponse(BaseModel):
    id: int = Field(
        gt=0,
        description="Уникальный идентификатор",
    )
    uri: str = Field(
        description="URI файла на сервере",
    )
    uploader_id: Optional[int] = Field(
        description="Идентификатор пользователя, загрузившего обложку"
    )
