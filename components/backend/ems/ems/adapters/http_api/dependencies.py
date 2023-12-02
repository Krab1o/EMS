from ems.application import services


class Services:
    event: services.EventService
    auth: services.AuthService
    event_type: services.EventTypeService


def get_event_service():
    return Services.event


def get_auth_service():
    return Services.auth


def get_event_type_service():
    return Services.event_type
