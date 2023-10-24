from typing import Optional

from attr import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import joinedload

from ems.application import entities
from ems.application.interfaces import IEventRepository


@dataclass
class EventRepository(IEventRepository):
    async_session_maker: async_sessionmaker

    async def get_list(self, page: int, size: int) -> list[entities.Event]:
        query = select(entities.Event).offset(page * size).limit(size)
        async with self.async_session_maker() as session:
            res = await session.execute(query)
        return res.scalars().all()

    async def get_one(self, event_id: int) -> Optional[entities.Event]:
        query = select(entities.Event)\
            .where(entities.Event.id == event_id)\
            .options(joinedload(entities.Event.type))\
            .options(
                joinedload(entities.Event.creator)
                .options(joinedload(entities.User.institution))
            )
        async with self.async_session_maker() as session:
            res = await session.execute(query)
        return res.scalar()
