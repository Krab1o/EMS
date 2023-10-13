from typing import Optional
from attr import dataclass
from datetime import datetime as dt

from ems.application.enum import (
    EventStatus,
    UserRole,
)


@dataclass
class Institution:
    id: int = None
    title: str = None
    description: Optional[str] = None


@dataclass
class User:
    id: int = None
    last_name: str = None
    first_name: str = None
    middle_name: Optional[str] = None
    institution_id: int = None
    institution: Institution = None
    course: Optional[int] = None
    group: Optional[int] = None
    role: UserRole = None
    telegram: Optional[str] = None
    vk: Optional[str] = None
    phone_number: Optional[str] = None
    email: str = None
    liked_events: list['Event'] = list()
    enrolled_in_events: list['Event'] = list()
    created_events: list['Event'] = list()


@dataclass
class EventType:
    id: int = None
    title: str = None
    description: Optional[str] = None


@dataclass
class Event:
    id: int = None
    title: str = None
    description: Optional[str] = None
    cover: Optional[str] = None
    status: EventStatus = None
    place: str = None
    datetime: dt = None
    creator_id: int = None
    creator: User = None
    voted_yes: int = None
    voted_no: int = None
    type_id: int = None
    type: EventType = None


@dataclass
class Club:
    id: int = None
    title: str = None
    description: Optional[str] = None
    place: str = None
