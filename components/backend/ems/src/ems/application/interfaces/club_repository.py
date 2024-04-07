from abc import ABC, abstractmethod
from typing import Optional

from ems.application import dto, entities


class IClubRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id_: int) -> Optional[entities.Club]:
        raise NotImplementedError

    @abstractmethod
    async def get_list(self, page: int, size: int) -> list[entities.Club]:
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, data: dto.ClubCreateRequest) -> Optional[int]:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, data: dto.ClubUpdateRequest) -> Optional[int]:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, club_id: int):
        raise NotImplementedError
