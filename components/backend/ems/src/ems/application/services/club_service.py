from enum import IntEnum, auto
from typing import Optional

from attr import dataclass
from ems.adapters.database.repositories import (
    ClubRepository,
    UserFavoriteClubRepository,
)
from ems.adapters.database.repositories.user_repository import UserRepository
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


class ClubFavoriteStatus(IntEnum):
    OK = auto()
    CLUB_NOT_FOUND = auto()
    USER_NOT_FOUND = auto()
    UNEXPECTED_ERROR = auto()


@dataclass
class ClubService:
    club_repository: ClubRepository
    user_repository: UserRepository
    user_favorite_club_repository: UserFavoriteClubRepository

    async def get_list(
            self,
            params: dto.PaginationParams,
            user_id: int,
    ) -> list[entities.Club]:
        clubs = await self.club_repository.get_list(
            page=params.page,
            size=params.size,
        )
        for club in clubs:
            user_fav_record = await self.user_favorite_club_repository.get_one(club.id, user_id)
            if user_fav_record is not None:
                club.is_favorite = True
        return clubs

    async def get_by_id(
            self,
            user_id: int,
            club_id: int,
    ) -> Optional[entities.Club]:
        db_club = await self.club_repository.get_by_id(club_id)
        if db_club is None:
            return None
        user_fav_record = await self.user_favorite_club_repository.get_one(club_id, user_id)
        if user_fav_record is not None:
            db_club.is_favorite = True
        return db_club

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

    async def star(
            self,
            club_id: int,
            user_id: int,
    ) -> ClubFavoriteStatus:
        db_club = await self.club_repository.get_by_id(club_id)
        if db_club is None:
            return ClubFavoriteStatus.CLUB_NOT_FOUND

        db_user = await self.user_repository.get_by_id(user_id)
        if db_user is None:
            return ClubFavoriteStatus.USER_NOT_FOUND

        user_favorite_club = await self.user_favorite_club_repository.get_one(
            club_id, user_id
        )
        if user_favorite_club is not None:
            await self.user_favorite_club_repository.delete_one(
                club_id, user_id
            )
        else:
            await self.user_favorite_club_repository.add_one(
                club_id, user_id
            )
        return ClubFavoriteStatus.OK
