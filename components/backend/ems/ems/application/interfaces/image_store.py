from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID, uuid4


class IImage:
    image_id: UUID
    size: int
    path: str


class IImageStore(ABC):
    @abstractmethod
    async def save(self, data: bytes, image_id: UUID, subdir: Optional[str] = None) -> IImage:
        raise NotImplementedError
