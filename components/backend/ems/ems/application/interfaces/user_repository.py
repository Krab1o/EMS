from abc import abstractmethod, ABC
from typing import Optional

from ems.application import entities, dto


class IUserRepository(ABC):
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
