from enum import IntEnum, auto
from typing import Final, Optional
from uuid import uuid4

import aiofiles
from attr import dataclass
from ems.adapters.database.repositories import (
    CoverRepository,
    EventRepository,
    EventTypeRepository,
    UserRepository,
    UserVotedEventRepository,
)
from ems.adapters.storage import ImageStore
from ems.application import dto, entities
from ems.application.entities import Cover
from ems.application.enum import EventStatus, UserRole
from fastapi import UploadFile


class EventCreateStatus(IntEnum):
    OK = auto()
    EVENT_TYPE_NOT_FOUND = auto()
    COVER_TOO_BIG = auto()
    UNEXPECTED_ERROR = auto()
    TOO_MANY_OPENED_EVENTS = auto()


class EventUpdateStatus(IntEnum):
    OK = auto()
    EVENT_NOT_FOUND = auto()
    COVER_NOT_FOUND = auto()
    FORBIDDEN = auto()
    UNEXPECTED_ERROR = auto()
    CONFLICT = auto()


class EventDeleteStatus(IntEnum):
    OK = auto()
    NOT_FOUND = auto()
    FORBIDDEN = auto()
    UNEXPECTED_ERROR = auto()


class EventVoteStatus(IntEnum):
    OK = auto()
    EVENT_NOT_FOUND = auto()
    USER_NOT_FOUND = auto()
    NOT_ON_POLL = auto()
    UNEXPECTED_ERROR = auto()


class CoverDownloadStatus(IntEnum):
    OK = auto()
    NOT_FOUND = auto()


@dataclass
class EventService:
    event_repository: EventRepository
    event_type_repository: EventTypeRepository
    user_voted_event_repository: UserVotedEventRepository
    user_repository: UserRepository
    cover_repository: CoverRepository
    image_store: ImageStore

    MAX_COVER_WIDTH: Final[int] = 1920
    MAX_COVER_HEIGHT: Final[int] = 1080
    MAX_COVER_SIZE: Final[int] = 10 * 1024 * 1024  # 10 MB

    async def get_list(
        self,
        params: dto.PaginationParams,
        user_id: int,
        event_type: Optional[list[int]] = None,
        status: Optional[list[EventStatus]] = None,
    ) -> list[entities.Event]:
        db_events = await self.event_repository.get_list(
            page=params.page,
            size=params.size,
            event_type=event_type,
            status=status,
        )

        for db_event in db_events:
            db_vote_record = await self.user_voted_event_repository.get_one(
                user_id=user_id,
                event_id=db_event.id,
            )
            if db_vote_record is not None:
                db_event.user_vote = db_vote_record.vote

        return db_events

    async def get_by_id(
        self,
        event_id: int,
        user_id: int,
        include_rejected: bool = False,
        include_on_review: bool = False,
    ) -> Optional[entities.Event]:
        db_event = await self.event_repository.get_by_id(
            event_id,
            include_rejected=include_rejected,
            include_on_review=include_on_review,
        )
        if db_event is None:
            return None

        db_vote_record = await self.user_voted_event_repository.get_one(
            user_id=user_id,
            event_id=db_event.id,
        )
        if db_vote_record is not None:
            db_event.user_vote = db_vote_record.vote

        return db_event

    async def add_one(
        self,
        event_data: dto.EventCreateRequest,
        creator_id: int,
        cover: Optional[UploadFile],
    ) -> tuple[Optional[int], EventCreateStatus]:
        event_type = await self.event_type_repository.get_by_id(
            event_data.type_id
        )
        if event_type is None:
            return None, EventCreateStatus.EVENT_TYPE_NOT_FOUND

        db_user = await self.user_repository.get_by_id(user_id=creator_id)

        if cover is not None and cover.size > self.MAX_COVER_SIZE:
            return None, EventCreateStatus.COVER_TOO_BIG

        on_review_count = (
            await self.event_repository.get_number_of_events_on_review(
                creator_id
            )
        )
        if on_review_count >= 2:
            return None, EventCreateStatus.TOO_MANY_OPENED_EVENTS

        event_id = await self.event_repository.add_one(
            event_data=event_data,
            creator_id=creator_id,
        )
        if not event_id:
            return None, EventCreateStatus.UNEXPECTED_ERROR

        db_event = await self.event_repository.get_by_id(
            event_id=event_id, include_on_review=True
        )

        if cover is not None:
            contents = await cover.read()
            await self.upload_cover(
                cover_bytes=contents,
                db_event=db_event,
                db_user=db_user,
            )

        return event_id, EventCreateStatus.OK

    async def update_one(
        self,
        data: dto.EventUpdateRequest,
        user_id: int,
        user_role: UserRole,
    ) -> EventUpdateStatus:
        match user_role:
            case UserRole.ADMIN:
                db_event = await self.event_repository.get_by_id(
                    event_id=data.id,
                    include_rejected=True,
                    include_on_review=True,
                )
            case UserRole.USER:
                db_event = await self.event_repository.get_by_id(
                    event_id=data.id,
                    include_on_review=True,
                )
            case _:
                return EventUpdateStatus.UNEXPECTED_ERROR

        if db_event is None:
            return EventUpdateStatus.EVENT_NOT_FOUND

        if data.cover_id is not None:
            db_cover = await self.cover_repository.get_by_id(data.cover_id)
            if db_cover is None:
                return EventUpdateStatus.COVER_NOT_FOUND

        if user_role != UserRole.ADMIN and db_event.creator_id != user_id:
            return EventUpdateStatus.FORBIDDEN

        if user_role != UserRole.ADMIN and data.status is not None:
            data.status = None

        if data.version - db_event.version != 1:
            return EventUpdateStatus.CONFLICT

        event_id = await self.event_repository.update_one(data)
        if event_id is None:
            return EventUpdateStatus.UNEXPECTED_ERROR
        return EventUpdateStatus.OK

    async def delete_one(
        self, event_id: int, user_id: int, user_role: UserRole
    ) -> EventDeleteStatus:
        match user_role:
            case UserRole.ADMIN:
                db_event = await self.event_repository.get_by_id(
                    event_id=event_id,
                    include_rejected=True,
                    include_on_review=True,
                )
            case UserRole.USER:
                db_event = await self.event_repository.get_by_id(
                    event_id=event_id,
                    include_on_review=True,
                )
            case _:
                return EventDeleteStatus.UNEXPECTED_ERROR

        if db_event is None:
            return EventDeleteStatus.NOT_FOUND

        if user_role != UserRole.ADMIN and db_event.creator_id != user_id:
            return EventDeleteStatus.FORBIDDEN

        await self.event_repository.delete_one(event_id)
        # TODO: delete cover
        return EventDeleteStatus.OK

    async def vote(
        self, data: dto.EventVoteRequest, event_id: int, user_id: int
    ) -> EventVoteStatus:
        db_event = await self.event_repository.get_by_id(event_id)

        if db_event is None:
            return EventVoteStatus.EVENT_NOT_FOUND
        if db_event.status != EventStatus.ON_POLL:
            return EventVoteStatus.NOT_ON_POLL

        db_user = await self.user_repository.get_by_id(user_id)
        if db_user is None:
            return EventVoteStatus.USER_NOT_FOUND

        # TODO: Возможны гонки данных. Вообще нужно реализовать
        #  механизм защиты от них, но для MVP пойдет.

        user_voted_event = await self.user_voted_event_repository.get_one(
            user_id, event_id
        )
        if user_voted_event is not None:
            await self.user_voted_event_repository.delete_one(
                user_id, event_id
            )
            if user_voted_event.vote:
                db_event.voted_yes -= 1
                await self.event_repository.update_vote_yes(
                    event_id, db_event.voted_yes
                )
            else:
                db_event.voted_no -= 1
                await self.event_repository.update_vote_no(
                    event_id, db_event.voted_no
                )

        await self.user_voted_event_repository.add_one(
            user_id, event_id, data.like
        )
        if data.like:
            await self.event_repository.update_vote_yes(
                event_id, db_event.voted_yes + 1
            )
        else:
            await self.event_repository.update_vote_no(
                event_id, db_event.voted_no + 1
            )

        return EventVoteStatus.OK

    async def upload_cover(
        self,
        cover_bytes: bytes,
        db_event: entities.Event,
        db_user: entities.User,
    ):
        image_id = uuid4()
        image = await self.image_store.save(
            cover_bytes, subdir="covers", image_id=image_id
        )

        db_cover = Cover(
            filename=f"{image_id}.jpeg",
            path=image.path,
            uploader_id=db_user.id,
        )

        cover_id = await self.cover_repository.add_one(db_cover)
        await self.event_repository.update_cover(db_event.id, cover_id)

    async def download_cover(
        self, cover_id: int
    ) -> tuple[Optional[bytes], CoverDownloadStatus]:
        db_cover = await self.cover_repository.get_by_id(cover_id=cover_id)
        if db_cover is None:
            return None, CoverDownloadStatus.NOT_FOUND

        async with aiofiles.open(db_cover.path, "rb") as img:
            res = await img.read()

        return res, CoverDownloadStatus.OK
