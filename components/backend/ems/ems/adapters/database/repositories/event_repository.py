from typing import Optional

from attr import dataclass

from sqlalchemy import select, insert, update, delete, func
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import joinedload

from ems.application import entities, dto
from ems.application.enum import EventStatus
from ems.application.interfaces import IEventRepository


@dataclass
class EventRepository(IEventRepository):
    async_session_maker: async_sessionmaker

    async def get_list(
            self,
            page: int, size: int,
            event_type: Optional[list[int]] = None,
            status: Optional[list[int]] = None
    ) -> list[entities.Event]:
        query = select(entities.Event)
        if event_type is not None:
            query = query.where(entities.Event.type_id.in_(event_type))
        if status is not None:
            query = query.where(entities.Event.status.in_(status))
        query = query\
            .offset(page * size)\
            .limit(size)\
            .options(joinedload(entities.Event.cover))

        async with self.async_session_maker() as session:
            res = await session.execute(query)
        return res.scalars().all()

    async def get_by_id(
            self,
            event_id: int,
            include_rejected: bool = False,
            include_on_review: bool = False,
    ) -> Optional[entities.Event]:
        query = select(entities.Event).where(entities.Event.id == event_id)
        if not include_rejected:
            query = query.where(entities.Event.status != EventStatus.REJECTED)
        if not include_on_review:
            query = query.where(entities.Event.status != EventStatus.ON_REVIEW)

        query = query\
            .options(joinedload(entities.Event.type))\
            .options(joinedload(entities.Event.cover))\
            .options(
                joinedload(entities.Event.creator)
                .options(joinedload(entities.User.institution))
            )\
            .options(
                joinedload(entities.Event.users_voted)
                .options(joinedload(entities.User.institution))
            )

        async with self.async_session_maker() as session:
            res = await session.execute(query)
        return res.scalar()

    async def add_one(self, creator_id: int, event_data: dto.EventCreateRequest) -> Optional[int]:
        async with self.async_session_maker() as session:
            to_insert = {
                **event_data.model_dump(),
                'status': EventStatus.ON_REVIEW,
                'creator_id': creator_id,
            }
            insert_query = insert(entities.Event).values(to_insert).returning(entities.Event.id)
            new_id = await session.scalar(insert_query)
            await session.commit()
        return new_id

    async def update_one(self, data: dto.EventUpdateRequest) -> Optional[int]:
        to_insert = data.model_dump(exclude={'id', 'status', 'cover_id'})
        if data.status is not None:
            to_insert['status'] = data.status
        if data.cover_id is not None:
            to_insert['cover_id'] = data.cover_id
        query = update(entities.Event)\
            .where(entities.Event.id == data.id)\
            .values(to_insert)\
            .returning(entities.Event.id)
        async with self.async_session_maker() as session:
            event_id = await session.scalar(query)
            await session.commit()
        return event_id

    async def delete_one(self, event_id: int):
        query = delete(entities.Event).where(entities.Event.id == event_id)
        async with self.async_session_maker() as session:
            await session.execute(query)
            await session.commit()

    async def update_vote_yes(self, event_id: int, new_value: int) -> Optional[int]:
        query = update(entities.Event)\
            .where(entities.Event.id == event_id)\
            .values({'voted_yes': new_value})\
            .returning(entities.Event.id)
        async with self.async_session_maker() as session:
            event_id = await session.scalar(query)
            await session.commit()
        return event_id

    async def update_vote_no(self, event_id: int, new_value: int) -> Optional[int]:
        query = update(entities.Event) \
            .where(entities.Event.id == event_id) \
            .values({'voted_no': new_value}) \
            .returning(entities.Event.id)
        async with self.async_session_maker() as session:
            event_id = await session.scalar(query)
            await session.commit()
        return event_id

    async def update_cover(self, event_id: int, cover_id: int) -> Optional[int]:
        query = update(entities.Event) \
            .where(entities.Event.id == event_id) \
            .values({'cover_id': cover_id}) \
            .returning(entities.Event.id)
        async with self.async_session_maker() as session:
            event_id = await session.scalar(query)
            await session.commit()
        return event_id

    async def get_number_of_events_on_review(self, user_id: int) -> Optional[int]:
        query = select(func.count()).select_from(entities.Event)\
                 .where(entities.Event.creator_id == user_id)\
                 .where(entities.Event.status == EventStatus.ON_REVIEW)

        async with self.async_session_maker() as session:
            res = await session.execute(query)
        return res.scalar()