from enum import IntEnum, auto
from typing import Optional

from attr import dataclass
from ems.adapters.database.repositories import (
    PlaceRepository,
)
from ems.adapters.database.repositories.institution_repository import (
    InstitutionRepository,
)
from ems.application import dto, entities


class PlaceCreateStatus(IntEnum):
    OK = auto()
    UNEXPECTED_ERROR = auto()


class PlaceUpdateStatus(IntEnum):
    OK = auto()
    PLACE_NOT_FOUND = auto()
    INSTITUTION_NOT_FOUND = auto()
    UNEXPECTED_ERROR = auto()


class PlaceDeleteStatus(IntEnum):
    OK = auto()
    NOT_FOUND = auto()
    UNEXPECTED_ERROR = auto()


@dataclass
class PlaceService:
    place_repository: PlaceRepository
    institution_repository: InstitutionRepository

    async def get_list(
            self,
            params: dto.PaginationParams,
    ) -> list[entities.Place]:
        places = await self.place_repository.get_list(
            page=params.page,
            size=params.size,
        )
        return places

    async def get_by_id(
            self,
            place_id: int,
    ) -> Optional[entities.Place]:
        db_place = await self.place_repository.get_by_id(place_id)
        if db_place is None:
            return None
        return db_place

    async def add_one(
            self,
            data: dto.PlaceCreateRequest,
    ) -> tuple[Optional[int], PlaceCreateStatus]:
        place_id = await self.place_repository.add_one(data=data)
        if not place_id:
            return None, PlaceCreateStatus.UNEXPECTED_ERROR
        return place_id, PlaceCreateStatus.OK

    async def update_one(
            self,
            data: dto.PlaceUpdateRequest,
    ) -> PlaceUpdateStatus:
        db_place = await self.place_repository.get_by_id(data.id)
        if db_place is None:
            return PlaceUpdateStatus.PLACE_NOT_FOUND
        
        if data.institution_id is not None:
            db_inst = await self.institution_repository.get_by_id(data.institution_id)
            if db_inst is None:
                return PlaceUpdateStatus.INSTITUTION_NOT_FOUND

        place_id = await self.place_repository.update_one(data)
        if place_id is None:
            return PlaceUpdateStatus.UNEXPECTED_ERROR
        return PlaceUpdateStatus.OK

    async def delete_one(
            self,
            place_id: int,
    ) -> PlaceDeleteStatus:
        db_place = await self.place_repository.get_by_id(place_id)
        if db_place is None:
            return PlaceDeleteStatus.NOT_FOUND

        await self.place_repository.delete_one(place_id)
        return PlaceDeleteStatus.OK
