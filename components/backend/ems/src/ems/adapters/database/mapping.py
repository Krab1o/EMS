from ems.adapters.database import tables
from ems.application import entities
from sqlalchemy.orm import backref, registry, relationship

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
        "institution": relationship(
            entities.Institution,
            foreign_keys=[tables.users.c.institution_id],
            lazy="select",
        ),
        "enrolled_in_events": relationship(
            entities.Event,
            secondary=tables.users_enrolled_in_events,
            lazy="select",
        ),
    },
)

mapper.map_imperatively(
    entities.Place,
    tables.places,
    properties={
        "institution": relationship(
            entities.Institution,
            foreign_keys=[tables.places.c.institution_id],
            lazy="select",
        ),
    }
)

mapper.map_imperatively(
    entities.Event,
    tables.events,
    properties={
        "creator": relationship(
            entities.User,
            foreign_keys=[tables.events.c.creator_id],
            backref=backref("created_events", lazy="select"),
            lazy="select",
        ),
        "type": relationship(
            entities.EventType,
            foreign_keys=[tables.events.c.type_id],
            lazy="select",
        ),
        "users_voted": relationship(
            entities.User,
            secondary=tables.users_voted_events,
            lazy="select",
        ),
        "cover": relationship(
            entities.Cover,
            foreign_keys=[tables.events.c.cover_id],
            lazy="select",
        ),
        "place": relationship(
            entities.Place,
            foreign_keys=[tables.events.c.place_id],
            lazy="select",
        )
    },
)

mapper.map_imperatively(
    entities.Club,
    tables.clubs,
    properties={
        "users_favorite": relationship(
            entities.User,
            secondary=tables.users_favorite_clubs,
            lazy="select",
        )
    }
)

mapper.map_imperatively(
    entities.UserFavoriteClub,
    tables.users_favorite_clubs,
)

mapper.map_imperatively(
    entities.UserVotedEvent,
    tables.users_voted_events,
)

mapper.map_imperatively(
    entities.Cover,
    tables.covers,
)
