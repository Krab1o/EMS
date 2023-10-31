from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from attr import dataclass

from ems.application import entities
from ems.application.interfaces import IEventTypeRepository


@dataclass
class EventTypeRepository(IEventTypeRepository):
    async_session_maker: async_sessionmaker

    async def get_by_id(self, id_: int) -> Optional[entities.EventType]:
        query = select(entities.EventType).where(entities.EventType.id == id_)
        async with self.async_session_maker() as session:
            res = await session.scalar(query)
        return res
