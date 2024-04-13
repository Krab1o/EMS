from enum import IntEnum, auto
from typing import Optional

from attr import dataclass
from ems.adapters.database.repositories import ClubRepository
from ems.application import dto, entities


class ClubCreateStatus(IntEnum):
    OK = auto()
    UNEXPECTED_ERROR = auto()


class ClubUpdateStatus(IntEnum):
    OK = auto()
    NOT_FOUND = auto()
    UNEXPECTED_ERROR = auto()


class ClubDeleteStatus(IntEnum):
    OK = auto()
    NOT_FOUND = auto()
    UNEXPECTED_ERROR = auto()


@dataclass
class ClubService:
    club_repository: ClubRepository

    async def get_list(
        self,
        params: dto.PaginationParams,
    ) -> list[entities.Club]:
        return await self.club_repository.get_list(
            page=params.page,
            size=params.size,
        )

    async def get_by_id(
        self,
        club_id: int,
    ) -> Optional[entities.Club]:
        return await self.club_repository.get_by_id(club_id)

    async def add_one(
        self,
        data: dto.ClubCreateRequest,
    ) -> tuple[Optional[int], ClubCreateStatus]:
        club_id = await self.club_repository.add_one(data=data)
        if not club_id:
            return None, ClubCreateStatus.UNEXPECTED_ERROR
        return club_id, ClubCreateStatus.OK

    async def update_one(
        self,
        data: dto.ClubUpdateRequest,
    ) -> ClubUpdateStatus:
        db_club = await self.club_repository.get_by_id(data.id)
        if db_club is None:
            return ClubUpdateStatus.NOT_FOUND
        event_id = await self.club_repository.update_one(data)
        if event_id is None:
            return ClubUpdateStatus.UNEXPECTED_ERROR
        return ClubUpdateStatus.OK

    async def delete_one(
        self,
        club_id: int,
    ) -> ClubDeleteStatus:
        db_club = await self.club_repository.get_by_id(club_id)
        if db_club is None:
            return ClubDeleteStatus.NOT_FOUND

        await self.club_repository.delete_one(club_id)
        return ClubDeleteStatus.OK
