from typing import Optional
from enum import IntEnum, auto

from attr import dataclass

from ems.application import dto, entities
from ems.application.interfaces import IEventTypeRepository


class EventTypeCreateStatus(IntEnum):
    OK = auto()
    UNEXPECTED_ERROR = auto()


class EventTypeUpdateStatus(IntEnum):
    OK = auto()
    NOT_FOUND = auto()
    UNEXPECTED_ERROR = auto()
    CONFLICT = auto()


class EventTypeDeleteStatus(IntEnum):
    OK = auto()
    NOT_FOUND = auto()
    UNEXPECTED_ERROR = auto()


@dataclass
class EventTypeService:
    event_type_repository: IEventTypeRepository

    async def get_list(
            self,
            params: dto.PaginationParams,
    ) -> list[entities.EventType]:
        return await self.event_type_repository.get_list(
            page=params.page,
            size=params.size,
        )

    async def get_by_id(
            self,
            event_type_id: int,
    ) -> Optional[entities.Event]:
        return await self.event_type_repository.get_by_id(event_type_id)

    async def add_one(
            self,
            data: dto.EventTypeCreateRequest,
    ) -> tuple[Optional[int], EventTypeCreateStatus]:
        event_type_id = await self.event_type_repository.add_one(data=data)
        if not event_type_id:
            return None, EventTypeCreateStatus.UNEXPECTED_ERROR
        return event_type_id, EventTypeCreateStatus.OK

    async def update_one(
            self,
            data: dto.EventTypeUpdateRequest,
    ) -> EventTypeUpdateStatus:
        db_event_type = await self.event_type_repository.get_by_id(data.id)
        if db_event_type is None:
            return EventTypeUpdateStatus.NOT_FOUND
        if data.version - db_event_type.version != 1:
            return EventTypeUpdateStatus.CONFLICT

        event_id = await self.event_type_repository.update_one(data)
        if event_id is None:
            return EventTypeUpdateStatus.UNEXPECTED_ERROR
        return EventTypeUpdateStatus.OK

    async def delete_one(
            self,
            event_type_id: int,
    ) -> EventTypeDeleteStatus:
        db_event_type = await self.event_type_repository.get_by_id(event_type_id)
        if db_event_type is None:
            return EventTypeDeleteStatus.NOT_FOUND

        await self.event_type_repository.delete_one(event_type_id)
        return EventTypeDeleteStatus.OK
