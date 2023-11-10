from typing import Optional
from enum import IntEnum, auto

from attr import dataclass

from ems.application import dto, entities
from ems.application.enum import EventStatus, UserRole
from ems.application.interfaces import IEventRepository, IEventTypeRepository


class EventCreateStatus(IntEnum):
    OK = auto()
    EVENT_TYPE_NOT_FOUND = auto()
    UNEXPECTED_ERROR = auto()


class EventUpdateStatus(IntEnum):
    OK = auto()
    NOT_FOUND = auto()
    FORBIDDEN = auto()
    UNEXPECTED_ERROR = auto()
    CONFLICT = auto()


class EventDeleteStatus(IntEnum):
    OK = auto()
    NOT_FOUND = auto()
    FORBIDDEN = auto()
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

    async def get_by_id(
            self,
            event_id: int,
            include_rejected: bool = False,
            include_on_review: bool = False,
    ) -> Optional[entities.Event]:
        return await self.event_repository.get_by_id(
            event_id,
            include_rejected=include_rejected,
            include_on_review=include_on_review,
        )

    async def add_one(
            self,
            event_data: dto.EventCreateRequest,
            creator_id: int,
    ) -> tuple[Optional[int], EventCreateStatus]:
        event_type = await self.event_type_repository.get_by_id(event_data.type_id)
        if event_type is None:
            return None, EventCreateStatus.EVENT_TYPE_NOT_FOUND

        event_id = await self.event_repository.add_one(event_data=event_data, creator_id=creator_id)
        if not event_id:
            return None, EventCreateStatus.UNEXPECTED_ERROR

        return event_id, EventCreateStatus.OK

    async def update_one(
            self,
            data: dto.EventUpdateRequest,
            user_id: int,
            user_role: UserRole,
    ) -> EventUpdateStatus:
        match user_role:
            case UserRole.ADMIN:
                db_event = await self.event_repository.get_by_id(data.id, include_rejected=True, include_on_review=True)
            case UserRole.USER:
                db_event = await self.event_repository.get_by_id(data.id, include_on_review=True)
            case _:
                return EventUpdateStatus.UNEXPECTED_ERROR

        if db_event is None:
            return EventUpdateStatus.NOT_FOUND

        if user_role != UserRole.ADMIN and db_event.creator_id != user_id:
            return EventUpdateStatus.FORBIDDEN

        if data.version - db_event.version != 1:
            return EventUpdateStatus.CONFLICT

        event_id = await self.event_repository.update_one(data)
        if event_id is None:
            return EventUpdateStatus.UNEXPECTED_ERROR
        return EventUpdateStatus.OK

    async def delete_one(self, event_id: int, user_id: int, user_role: UserRole) -> EventDeleteStatus:
        match user_role:
            case UserRole.ADMIN:
                db_event = await self.event_repository.get_by_id(event_id, include_rejected=True, include_on_review=True)
            case UserRole.USER:
                db_event = await self.event_repository.get_by_id(event_id, include_on_review=True)
            case _:
                return EventDeleteStatus.UNEXPECTED_ERROR

        if db_event is None:
            return EventDeleteStatus.NOT_FOUND

        if user_role != UserRole.ADMIN and db_event.creator_id != user_id:
            return EventDeleteStatus.FORBIDDEN

        await self.event_repository.delete_one(event_id)
        return EventDeleteStatus.OK
