from enum import StrEnum, auto


class UserRole(StrEnum):
    USER = auto()
    ADMIN = auto()


class EventStatus(StrEnum):
    ON_REVIEW = auto()
    REJECTED = auto()
    ON_POLL = auto()
    PLANNED = auto()
    CANCELLED = auto()
    ENDED = auto()
