from typing import Optional

from attr import dataclass
from ems.application import entities
from ems.application.entities import Cover
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker


@dataclass
class CoverRepository:
    async_session_maker: async_sessionmaker

    async def get_by_id(self, cover_id: int) -> Optional[entities.Cover]:
        query = select(entities.Cover).where(entities.Cover.id == cover_id)
        async with self.async_session_maker() as session:
            res = await session.scalar(query)
        return res

    async def add_one(self, data: Cover) -> int:
        async with self.async_session_maker() as session:
            session.add(data)
            await session.commit()
            await session.refresh(data, ("id",))
        return data.id
