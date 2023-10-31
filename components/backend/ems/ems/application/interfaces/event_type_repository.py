from abc import ABC, abstractmethod
from typing import Optional

from ems.application import entities


class IEventTypeRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id_: int) -> Optional[entities.EventType]:
        raise NotImplementedError
