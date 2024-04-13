from datetime import datetime
from typing import Optional

from attr import dataclass
from ems.application import dto, entities
from ems.application.enum import UserRole
from ems_libs.security import Hasher
from sqlalchemy import delete, insert, or_, select, update
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import joinedload


@dataclass
class UserRepository:
    async_session_maker: async_sessionmaker

    async def is_email_taken(self, email: str) -> bool:
        query = select(entities.User).where(entities.User.email == email)
        async with self.async_session_maker() as session:
            db_user = await session.scalar(query)
        return db_user is not None

    async def get_by_email(self, email: str) -> Optional[entities.User]:
        query = (
            select(entities.User)
            .where(entities.User.email == email)
            .options(joinedload(entities.User.institution))
            .options(joinedload(entities.User.enrolled_in_events))
            .options(joinedload(entities.User.created_events))
        )
        async with self.async_session_maker() as session:
            db_user = await session.scalar(query)
        return db_user

    async def get_by_id(self, user_id: int) -> Optional[entities.User]:
        query = (
            select(entities.User)
            .where(entities.User.id == user_id)
            .options(joinedload(entities.User.institution))
            .options(joinedload(entities.User.enrolled_in_events))
            .options(joinedload(entities.User.created_events))
        )
        async with self.async_session_maker() as session:
            db_user = await session.scalar(query)
        return db_user

    async def add_one(self, data: dto.UserCreateRequest) -> Optional[int]:
        to_insert = {
            **data.model_dump(exclude={"password"}),
            "password": Hasher.get_hash(data.password),
            "role": UserRole.USER,
            "created_at": datetime.now(),
        }
        insert_query = (
            insert(entities.User).values(to_insert).returning(entities.User.id)
        )

        async with self.async_session_maker() as session:
            new_id = await session.scalar(insert_query)
            await session.commit()
        return new_id

    async def get_list(
        self,
        page: int,
        size: int,
    ) -> list[entities.User]:
        query = (
            select(entities.User)
            .order_by(entities.User.created_at)
            .options(joinedload(entities.User.institution))
            .options(joinedload(entities.User.enrolled_in_events))
            .options(joinedload(entities.User.created_events))
            .offset(page * size)
            .limit(size)
        )

        async with self.async_session_maker() as session:
            res = await session.execute(query)
        return res.unique().scalars().all()

    async def update_one(self, data: dto.UserUpdateRequest) -> Optional[int]:
        query = (
            update(entities.User)
            .where(entities.User.id == data.id)
            .values(data.model_dump(exclude={"id"}))
            .returning(entities.User.id)
        )
        async with self.async_session_maker() as session:
            user_id = await session.scalar(query)
            await session.commit()
        return user_id

    async def delete_one(self, user_id: int):
        query = delete(entities.User).where(entities.User.id == user_id)
        async with self.async_session_maker() as session:
            await session.execute(query)
            await session.commit()

    async def find(
        self,
        page: int | None = None,
        size: int | None = None,
        name_search: str | None = None,
        email_search: str | None = None
    ) -> list[entities.User]:
        query = (
            select(entities.User)
                .options(joinedload(entities.User.institution))
                .options(joinedload(entities.User.enrolled_in_events))
                .options(joinedload(entities.User.created_events))
        )
        if name_search is not None:
            query = query.where(
                or_(
                    entities.User.first_name.like(
                        f"%{name_search}%"
                    ),
                    entities.User.last_name.like(
                        f"%{name_search}%"
                    ),
                    entities.User.middle_name.like(
                        f"%{name_search}%"
                    )
                )
            )
        if email_search is not None:
            query = query.where(
                entities.User.email.like(f"%{email_search}%")
            )
        if page is not None and size is not None:
            query = query.offset(page * size).limit(size)
        async with self.async_session_maker() as session:
            res = await session.execute(query)
        return res.unique().scalars().all()
