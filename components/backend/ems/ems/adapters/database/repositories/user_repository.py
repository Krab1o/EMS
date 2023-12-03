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
            .options(joinedload(entities.User.enrolled_in_events))\
            .options(joinedload(entities.User.created_events))
        async with self.async_session_maker() as session:
            db_user = await session.scalar(query)
        return db_user

    async def get_by_id(self, id_: int) -> Optional[entities.User]:
        query = select(entities.User)\
            .where(entities.User.id == id_)\
            .options(joinedload(entities.User.institution))\
            .options(joinedload(entities.User.enrolled_in_events))\
            .options(joinedload(entities.User.created_events))
        async with self.async_session_maker() as session:
            db_user = await session.scalar(query)
        return db_user

    async def add_one(self, data: dto.UserCreateRequest) -> Optional[int]:
        to_insert = {
            **data.model_dump(exclude={'password'}),
            'password': Hasher.get_hash(data.password),
            'role': UserRole.USER,
        }
        insert_query = insert(entities.User).values(to_insert).returning(entities.User.id)

        async with self.async_session_maker() as session:
            new_id = await session.scalar(insert_query)
            await session.commit()
        return new_id
