import aiohttp
from ems.adapters.http_api.settings import Settings as HttpSettings
from ems.application import services


class Services:
    event: services.EventService
    auth: services.AuthService
    event_type: services.EventTypeService
    user: services.UserService
    club: services.ClubService
    place: services.PlaceService


class Sessions:
    http_session: aiohttp.ClientSession


class Settings:
    http_settings: HttpSettings


def get_event_service():
    return Services.event


def get_auth_service():
    return Services.auth


def get_event_type_service():
    return Services.event_type


def get_user_service():
    return Services.user


def get_club_service():
    return Services.club


def get_place_service():
    return Services.place


def get_http_session():
    return Sessions.http_session

def get_http_settings():
    return Settings.http_settings
