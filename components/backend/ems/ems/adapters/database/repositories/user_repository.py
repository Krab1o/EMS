from typing import Optional

from attr import dataclass

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import joinedload

from ems.application import entities, dto
from ems.application.enum import UserRole
from ems.application.interfaces import IUserRepository
from ems_libs.security import Hasher


@dataclass
class UserRepository(IUserRepository):
    async_session_maker: async_sessionmaker

    async def is_email_taken(self, email: str) -> bool:
        query = select(entities.User).where(entities.User.email == email)
        async with self.async_session_maker() as session:
            db_user = await session.scalar(query)
        return db_user is not None

    async def get_by_email(self, email: str) -> Optional[entities.User]:
        query = select(entities.User)\
            .where(entities.User.email == email)\
            .options(joinedload(entities.User.institution))\
            .options(joinedload(entities.User.liked_events))\
            .options(joinedload(entities.User.enrolled_in_events))\
            .options(joinedload(entities.User.created_events))
        async with self.async_session_maker() as session:
            db_user = await session.scalar(query)
        return db_user

    async def add_one(self, data: dto.UserCreateRequest) -> entities.User:
        to_insert = data.model_dump(exclude={'password'})
        to_insert['password'] = Hasher.get_hash(data.password)
        to_insert['role'] = UserRole.USER
        print(to_insert)
        insert_query = insert(entities.User).values(to_insert).returning(entities.User.id)

        async with self.async_session_maker() as session:
            new_id = await session.scalar(insert_query)
            await session.commit()

            fetch_query = select(entities.User) \
                .where(entities.User.id == new_id) \
                .options(joinedload(entities.User.institution)) \
                .options(joinedload(entities.User.liked_events)) \
                .options(joinedload(entities.User.enrolled_in_events)) \
                .options(joinedload(entities.User.created_events))
            db_user = await session.scalar(fetch_query)

        return db_user
