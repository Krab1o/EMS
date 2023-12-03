from sqlalchemy.orm import registry, relationship, backref

from ems.adapters.database import tables
from ems.application import entities

mapper = registry()

mapper.map_imperatively(
    entities.Institution,
    tables.institutions,
)

mapper.map_imperatively(
    entities.EventType,
    tables.event_types,
)

mapper.map_imperatively(
    entities.User,
    tables.users,
    properties={
        'institution': relationship(
            entities.Institution,
            foreign_keys=[tables.users.c.institution_id],
            lazy='select',
        ),
        'enrolled_in_events': relationship(
            entities.Event,
            secondary=tables.users_enrolled_in_events,
            lazy='select',
        ),
    }
)

mapper.map_imperatively(
    entities.Event,
    tables.events,
    properties={
        'creator': relationship(
            entities.User,
            foreign_keys=[tables.events.c.creator_id],
            backref=backref('created_events', lazy='select'),
            lazy='select',
        ),
        'type': relationship(
            entities.EventType,
            foreign_keys=[tables.events.c.type_id],
            lazy='select',
        ),
        'users_voted': relationship(
            entities.User,
            secondary=tables.users_voted_events,
            lazy='select',
        ),
    }
)

mapper.map_imperatively(
    entities.Club,
    tables.clubs,
)

mapper.map_imperatively(
    entities.UserVotedEvent,
    tables.users_voted_events,
)
