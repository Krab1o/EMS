from datetime import datetime
from typing import Optional

from attr import dataclass
from ems.application import dto, entities
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import joinedload


@dataclass
class PlaceRepository:
    async_session_maker: async_sessionmaker

    async def get_by_id(self, place_id: int) -> Optional[entities.Place]:
        query = (
            select(entities.Place)
            .options(
                joinedload(entities.Place.institution)
            )
            .where(entities.Place.id == place_id)
        )
        async with self.async_session_maker() as session:
            db_club = await session.scalar(query)
        return db_club

    async def get_list(self, page: int, size: int) -> list[entities.Place]:
        query = (
            select(entities.Place)
            .options(
                joinedload(entities.Place.institution)
            )
            .order_by(entities.Place.created_at)
            .offset(page * size)
            .limit(size)
        )
        async with self.async_session_maker() as session:
            res = await session.execute(query)
        return res.unique().scalars().all()

    async def add_one(self, data: dto.PlaceCreateRequest) -> Optional[int]:
        to_insert = {
            **data.model_dump(),
            "created_at": datetime.now(),
        }
        query = (
            insert(entities.Place)
            .values(to_insert)
            .returning(entities.Place.id)
        )
        async with self.async_session_maker() as session:
            new_id = await session.scalar(query)
            await session.commit()
        return new_id

    async def update_one(self, data: dto.PlaceUpdateRequest) -> Optional[int]:
        query = (
            update(entities.Place)
            .where(entities.Place.id == data.id)
            .values(data.model_dump(exclude={"id"}))
            .returning(entities.Place.id)
        )
        async with self.async_session_maker() as session:
            place_id = await session.scalar(query)
            await session.commit()
        return place_id 

    async def delete_one(self, place_id: int):
        query = delete(entities.Place).where(entities.Place.id == place_id)
        async with self.async_session_maker() as session:
            await session.execute(query)
            await session.commit()
