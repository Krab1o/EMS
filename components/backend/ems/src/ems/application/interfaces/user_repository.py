from abc import ABC, abstractmethod
from typing import Optional

from ems.application import dto, entities


class IUserRepository(ABC):
    @abstractmethod
    async def get_list(
        self,
        page: int,
        size: int,
    ) -> list[entities.User]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[entities.User]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[entities.User]:
        raise NotImplementedError

    @abstractmethod
    async def is_email_taken(self, email: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, data: dto.UserCreateRequest) -> Optional[int]:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, data: dto.UserUpdateRequest) -> Optional[int]:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, user_id: int):
        raise NotImplementedError
