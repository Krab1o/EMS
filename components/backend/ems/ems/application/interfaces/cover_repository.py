from abc import ABC, abstractmethod
from typing import Optional

from ems.application import entities
from ems.application.entities import Cover


class ICoverRepository(ABC):
    @abstractmethod
    async def get_by_id(self, cover_id: int) -> Optional[entities.Cover]:
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, data: Cover) -> int:
        raise NotImplementedError
