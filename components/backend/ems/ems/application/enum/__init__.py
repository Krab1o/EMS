from enum import StrEnum, auto


class UserRole(StrEnum):
    USER = auto()
    ADMIN = auto()


class EventStatus(StrEnum):
    ON_POLL = auto()
    CANCELLED = auto()
    ON_REVIEW = auto()
    PLANNED = auto()
    ENDED = auto()
