from ems.application import services


class Services:
    event: services.EventService
    auth: services.AuthService
    event_type: services.EventTypeService
    user: services.UserService
    club: services.ClubService

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
