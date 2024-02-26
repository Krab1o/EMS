from typing import Optional

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import async_sessionmaker

from attr import dataclass

from ems.application import entities, dto
from ems.application.interfaces import IClubRepository


@dataclass
class ClubRepository(IClubRepository):
    async_session_maker: async_sessionmaker

    async def get_by_id(self, id_: int) -> Optional[entities.Club]:
        query = select(entities.Club).where(entities.Club.id == id_)
        async with self.async_session_maker() as session:
            res = await session.scalar(query)
        return res

    async def get_list(self, page: int, size: int) -> list[entities.Club]:
        query = select(entities.Club) \
            .offset(page * size) \
            .limit(size)
        async with self.async_session_maker() as session:
            res = await session.execute(query)
        return res.scalars().all()

    async def add_one(self, data: dto.ClubCreateRequest) -> Optional[int]:
        query = insert(entities.Club) \
            .values(**data.model_dump()) \
            .returning(entities.Club.id)
        async with self.async_session_maker() as session:
            new_id = await session.scalar(query)
            await session.commit()
        return new_id

    async def update_one(self, data: dto.ClubUpdateRequest) -> Optional[int]:
        query = update(entities.Club) \
            .where(entities.Club.id == data.id) \
            .values(data.model_dump(exclude={'id'})) \
            .returning(entities.Club.id)
        async with self.async_session_maker() as session:
            club_id = await session.scalar(query)
            await session.commit()
        return club_id

    async def delete_one(self, club_id: int):
        query = delete(entities.Club) \
            .where(entities.Club.id == club_id)
        async with self.async_session_maker() as session:
            await session.execute(query)
            await session.commit()
