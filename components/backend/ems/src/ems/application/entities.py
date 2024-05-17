from datetime import datetime as dt
from typing import Optional

from attr import dataclass
from ems.application.enum import (
    EventStatus,
    UserRole,
)


@dataclass
class Institution:
    id: int = None
    title: str = None
    description: Optional[str] = None
    version: int = None


@dataclass
class User:
    id: int = None
    last_name: str = None
    first_name: str = None
    middle_name: Optional[str] = None
    institution_id: Optional[int] = None
    institution: Institution = None
    course: Optional[int] = None
    group: Optional[int] = None
    role: UserRole = None
    telegram: Optional[str] = None
    vk: Optional[str] = None
    phone_number: Optional[str] = None
    email: str = None
    password: str = None
    enrolled_in_events: list["Event"] = list()
    created_events: list["Event"] = list()
    version: int = None
    created_at: dt = None


@dataclass
class EventType:
    id: int = None
    title: str = None
    description: Optional[str] = None
    version: int = None


@dataclass
class Place:
    id: int = None
    title: str = None
    floor: Optional[int] = None
    institution_id: Optional[int] = None
    institution: Optional[Institution] = None
    created_at: dt = None


@dataclass
class Event:
    id: int = None
    title: str = None
    description: Optional[str] = None
    cover_id: Optional[int] = None
    cover: Optional["Cover"] = None
    status: EventStatus = None
    place: Place = None
    place_id: int = None
    datetime: dt = None
    dateend: dt = None
    creator_id: int = None
    creator: User = None
    voted_yes: int = None
    voted_no: int = None
    type_id: int = None
    type: EventType = None
    users_voted: list[User] = None
    user_vote: Optional[bool] = None
    created_at: dt = None


@dataclass
class UserVotedEvent:
    user_id: int = None
    event_id: int = None
    vote: bool = None
    created_at: dt = None


@dataclass
class Cover:
    id: int = None
    filename: str = None
    path: str = None
    uploader_id: int = None


@dataclass
class Club:
    id: int = None
    title: str = None
    description: str = None
    telegram: Optional[str] = None
    vk: Optional[str] = None
    youtube: Optional[str] = None
    rutube: Optional[str] = None
    tiktok: Optional[str] = None
    created_at: dt = None
    users_favorite: list[User] = None
    is_favorite: bool = False


@dataclass
class UserFavoriteClub:
    user_id: int = None
    club_id: int = None
