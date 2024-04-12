from datetime import datetime
from typing import Optional

from attr import dataclass
from ems.application import dto, entities
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import joinedload


@dataclass
class ClubRepository:
    async_session_maker: async_sessionmaker

    async def get_by_id(self, club_id: int) -> Optional[entities.Club]:
        query = (
            select(entities.Club)
            .options(
                joinedload(entities.Club.users_favorite)
                .options(
                    joinedload(entities.User.institution)
                )
            )
            .where(entities.Club.id == club_id)
        )
        async with self.async_session_maker() as session:
            db_club = await session.scalar(query)
        return db_club

    async def get_list(self, page: int, size: int) -> list[entities.Club]:
        query = (
            select(entities.Club)
            .order_by(entities.Club.created_at)
            .offset(page * size)
            .limit(size)
        )
        async with self.async_session_maker() as session:
            res = await session.execute(query)
        return res.scalars().all()

    async def add_one(self, data: dto.ClubCreateRequest) -> Optional[int]:
        to_insert = {
            **data.model_dump(),
            "created_at": datetime.now(),
        }
        query = (
            insert(entities.Club)
            .values(to_insert)
            .returning(entities.Club.id)
        )
        async with self.async_session_maker() as session:
            new_id = await session.scalar(query)
            await session.commit()
        return new_id

    async def update_one(self, data: dto.ClubUpdateRequest) -> Optional[int]:
        query = (
            update(entities.Club)
            .where(entities.Club.id == data.id)
            .values(data.model_dump(exclude={"id"}))
            .returning(entities.Club.id)
        )
        async with self.async_session_maker() as session:
            club_id = await session.scalar(query)
            await session.commit()
        return club_id

    async def delete_one(self, club_id: int):
        query = delete(entities.Club).where(entities.Club.id == club_id)
        async with self.async_session_maker() as session:
            await session.execute(query)
            await session.commit()
