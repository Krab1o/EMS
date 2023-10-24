from abc import ABC, abstractmethod
from typing import Optional

from ems.application import entities


class IEventRepository(ABC):
    @abstractmethod
    async def get_list(self, page: int, size: int) -> list[entities.Event]:
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, event_id: int) -> Optional[entities.Event]:
        raise NotImplementedError
