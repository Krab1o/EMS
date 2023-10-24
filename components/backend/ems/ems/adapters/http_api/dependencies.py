from ems.application import services


class Services:
    event: services.EventService
    auth: services.AuthService


def get_event_service():
    return Services.event


def get_auth_service():
    return Services.auth
