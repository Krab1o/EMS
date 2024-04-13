from typing import Optional

from attr import dataclass
from ems.application import entities
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import async_sessionmaker


@dataclass
class UserFavoriteClubRepository:
    async_session_maker: async_sessionmaker

    async def get_one(self, club_id: int, user_id: int) -> Optional[entities.UserFavoriteClub]:
        query = (
            select(entities.UserFavoriteClub)
            .where(entities.UserFavoriteClub.club_id == club_id)
            .where(entities.UserFavoriteClub.user_id == user_id)
        )
        async with self.async_session_maker() as session:
            res = await session.scalar(query)
        return res

    async def add_one(self, club_id: int, user_id: int):
        query = (
            insert(entities.UserFavoriteClub)
            .values({"user_id": user_id, "club_id": club_id})
        )
        async with self.async_session_maker() as session:
            await session.execute(query)
            await session.commit()

    async def delete_one(self, club_id: int, user_id: int):
        query = (
            delete(entities.UserFavoriteClub)
            .where(entities.UserFavoriteClub.club_id == club_id)
            .where(entities.UserFavoriteClub.user_id == user_id)
        )
        async with self.async_session_maker() as session:
            await session.execute(query)
            await session.commit()
