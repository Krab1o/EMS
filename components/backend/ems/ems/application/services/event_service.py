from typing import Optional
from enum import IntEnum, auto

from attr import dataclass

from ems.application import dto, entities
from ems.application.enum import EventStatus
from ems.application.interfaces import IEventRepository, IEventTypeRepository


class EventCreateStatus(IntEnum):
    OK = auto()
    EVENT_TYPE_NOT_FOUND = auto()
    UNEXPECTED_ERROR = auto()


@dataclass
class EventService:
    event_repository: IEventRepository
    event_type_repository: IEventTypeRepository

    async def get_list(
            self,
            params: dto.PaginationParams,
            event_type: Optional[list[int]] = None,
            status: Optional[list[EventStatus]] = None,
    ) -> list[entities.Event]:
        return await self.event_repository.get_list(
            page=params.page,
            size=params.size,
            event_type=event_type,
            status=status,
        )

    async def get_by_id(self, event_id: int, include_rejected: bool = False):
        return await self.event_repository.get_by_id(event_id, include_rejected)

    async def add_one(
            self,
            creator_id: int,
            event_data: dto.EventCreateRequest
    ) -> tuple[Optional[int], EventCreateStatus]:
        event_type = await self.event_type_repository.get_by_id(event_data.type_id)
        if event_type is None:
            return None, EventCreateStatus.EVENT_TYPE_NOT_FOUND

        event_id = await self.event_repository.add_one(creator_id, event_data)
        if not event_id:
            return None, EventCreateStatus.UNEXPECTED_ERROR

        return event_id, EventCreateStatus.OK
