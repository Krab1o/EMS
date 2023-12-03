from typing import Optional

from sqlalchemy import insert, delete, select
from sqlalchemy.ext.asyncio import async_sessionmaker

from attr import dataclass
from datetime import datetime

from ems.application import entities
from ems.application.interfaces import IUserVotedEventRepository


@dataclass
class UserVotedEventRepository(IUserVotedEventRepository):
    async_session_maker: async_sessionmaker

    async def add_one(self, user_id: int, event_id: int, vote: bool) -> Optional[int]:
        to_insert = {
            'user_id': user_id,
            'event_id': event_id,
            'vote': vote,
            'created_at': datetime.now(),
        }
        query = insert(entities.UserVotedEvent) \
            .values(to_insert) \
            .returning(entities.UserVotedEvent.user_id)
        async with self.async_session_maker() as session:
            new_id = await session.scalar(query)
            await session.commit()
        return new_id

    async def delete_one(self, user_id: int, event_id: int):
        query = delete(entities.UserVotedEvent)\
            .where(
                entities.UserVotedEvent.user_id == user_id,
                entities.UserVotedEvent.event_id == event_id,
            )
        async with self.async_session_maker() as session:
            await session.execute(query)
            await session.commit()

    async def get_one(self, user_id: int, event_id: int) -> Optional[entities.UserVotedEvent]:
        query = select(entities.UserVotedEvent)\
            .where(
                entities.UserVotedEvent.user_id == user_id,
                entities.UserVotedEvent.event_id == event_id,
            )
        async with self.async_session_maker() as session:
            res = await session.scalar(query)
        return res
