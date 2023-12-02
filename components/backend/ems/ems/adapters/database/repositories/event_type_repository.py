from typing import Optional

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import async_sessionmaker

from attr import dataclass

from ems.application import entities, dto
from ems.application.interfaces import IEventTypeRepository


@dataclass
class EventTypeRepository(IEventTypeRepository):
    async_session_maker: async_sessionmaker

    async def get_by_id(self, id_: int) -> Optional[entities.EventType]:
        query = select(entities.EventType).where(entities.EventType.id == id_)
        async with self.async_session_maker() as session:
            res = await session.scalar(query)
        return res

    async def get_list(self, page: int, size: int) -> list[entities.EventType]:
        query = select(entities.EventType) \
            .offset(page * size) \
            .limit(size)
        async with self.async_session_maker() as session:
            res = await session.execute(query)
        return res.scalars().all()

    async def add_one(self, data: dto.EventTypeCreateRequest) -> Optional[int]:
        query = insert(entities.EventType) \
            .values(**data.model_dump()) \
            .returning(entities.EventType.id)
        async with self.async_session_maker() as session:
            new_id = await session.scalar(query)
            await session.commit()
        return new_id

    async def update_one(self, data: dto.EventTypeUpdateRequest) -> Optional[int]:
        query = update(entities.EventType) \
            .where(entities.EventType.id == data.id) \
            .values(data.model_dump(exclude={'id'})) \
            .returning(entities.EventType.id)
        async with self.async_session_maker() as session:
            event_type_id = await session.scalar(query)
            await session.commit()
        return event_type_id

    async def delete_one(self, event_type_id: int):
        query = delete(entities.EventType) \
            .where(entities.EventType.id == event_type_id)
        async with self.async_session_maker() as session:
            await session.execute(query)
            await session.commit()
