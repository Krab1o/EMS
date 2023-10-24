from typing import Optional

from attr import dataclass

from ems.application import dto, entities
from ems.application.interfaces import IEventRepository


@dataclass
class EventService:
    event_repository: IEventRepository

    async def get_list(self, params: dto.PaginationParams) -> list[entities.Event]:
        return await self.event_repository.get_list(params.page, params.size)

    async def get_one(self, event_id: int) -> Optional[entities.Event]:
        return await self.event_repository.get_one(event_id)
