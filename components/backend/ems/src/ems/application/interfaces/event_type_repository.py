from abc import ABC, abstractmethod
from typing import Optional

from ems.application import dto, entities


class IEventTypeRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id_: int) -> Optional[entities.EventType]:
        raise NotImplementedError

    @abstractmethod
    async def get_list(self, page: int, size: int) -> list[entities.EventType]:
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, data: dto.EventTypeCreateRequest) -> Optional[int]:
        raise NotImplementedError

    @abstractmethod
    async def update_one(
        self, data: dto.EventTypeUpdateRequest
    ) -> Optional[int]:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, event_type_id: int):
        raise NotImplementedError
