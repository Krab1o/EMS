from typing import Optional, Final
from enum import IntEnum, auto

from attr import dataclass

from ems.application import dto, entities
from ems.application.enum import UserRole
from ems.application.interfaces import (
    IUserRepository, IInstitutionRepository
)

class UserCreateStatus(IntEnum):
    OK = auto()
    INSTITUTION_NOT_FOUND = auto()
    UNEXPECTED_ERROR = auto()

class UserUpdateStatus(IntEnum):
    OK = auto()
    USER_NOT_FOUND = auto()
    INSTITUTION_NOT_FOUND = auto()
    UNEXPECTED_ERROR = auto()
    CONFLICT = auto()

class UserDeleteStatus(IntEnum):
    OK = auto()
    NOT_FOUND = auto()
    UNEXPECTED_ERROR = auto()

@dataclass
class UserService:
    user_repository: IUserRepository
    institution_repository: IInstitutionRepository

    async def get_list(
            self,
            params: dto.PaginationParams,
    ) -> list[entities.User]:
        return await self.user_repository.get_list(
            page=params.page,
            size=params.size,
        )

    async def get_by_id(
            self,
            user_id: int,
    ) -> Optional[entities.User]:
        db_user = await self.user_repository.get_by_id(
            user_id,
        )

        if db_user is None:
            return None

        return db_user

    async def add_one(
            self,
            data: dto.UserCreateRequest,
    ) -> tuple[Optional[int], UserCreateStatus]:
        institution = await self.institution_repository.get_by_id(data.institution_id)
        if institution is None:
            return None, UserCreateStatus.INSTITUTION_NOT_FOUND

        user_id = await self.user_repository.add_one(
            data=data
        )
        if not user_id:
            return None, UserCreateStatus.UNEXPECTED_ERROR

        return user_id, UserCreateStatus.OK

    async def update_one(
            self,
            data: dto.UserUpdateRequest,
    ) -> UserUpdateStatus:

        db_user = await self.user_repository.get_by_id(
            user_id=data.id,
        )
        if db_user is None:
            return UserUpdateStatus.EVENT_NOT_FOUND

        event_id = await self.user_repository.update_one(data)

        if data.version - db_user.version != 1:
            return UserUpdateStatus.CONFLICT

        if event_id is None:
            return UserUpdateStatus.UNEXPECTED_ERROR
        return UserUpdateStatus.OK

    async def delete_one(self, user_id: int) -> UserDeleteStatus:
        db_event = await self.user_repository.get_by_id(
            user_id=user_id,
        )

        if db_event is None:
            return UserDeleteStatus.NOT_FOUND

        await self.user_repository.delete_one(user_id)
        return UserDeleteStatus.OK