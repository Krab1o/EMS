from abc import ABC, abstractmethod
from typing import Optional

from ems.application import entities


class IUserVotedEventRepository(ABC):
    @abstractmethod
    async def get_one(
        self, user_id: int, event_id: int
    ) -> Optional[entities.UserVotedEvent]:
        raise NotImplementedError

    @abstractmethod
    async def add_one(
        self, user_id: int, event_id: int, vote: bool
    ) -> Optional[int]:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, user_id: int, event_id: int):
        raise NotImplementedError
