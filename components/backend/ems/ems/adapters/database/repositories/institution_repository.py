from typing import Optional
from attr import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from ems.application import entities
from ems.application.interfaces import IInstitutionRepository


@dataclass
class InstitutionRepository(IInstitutionRepository):
    async_session_maker: async_sessionmaker

    async def get_by_id(self, id_: int) -> Optional[entities.Institution]:
        query = select(entities.Institution).where(entities.Institution.id == id_)
        async with self.async_session_maker() as session:
            institution = await session.scalar(query)
        return institution
