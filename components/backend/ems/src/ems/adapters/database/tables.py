from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
)

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=naming_convention)

users = Table(
    "users",
    metadata,
    Column(
        "id", Integer, primary_key=True, comment="Уникальный идентификатор"
    ),
    Column("last_name", String(128), nullable=False, comment="Фамилия"),
    Column("first_name", String(128), nullable=False, comment="Имя"),
    Column(
        "middle_name",
        String(128),
        nullable=True,
        default=None,
        comment="Отчество",
    ),
    Column(
        "institution_id",
        ForeignKey("institutions.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
        comment="Идентификатор факультета/института, к которому относится пользователь",
    ),
    Column(
        "course", Integer, nullable=True, default=None, comment="Номер курса"
    ),
    Column(
        "group", Integer, nullable=True, default=None, comment="Номер группы"
    ),
    Column("role", String(64), nullable=False, comment="Роль"),
    Column(
        "telegram",
        String(128),
        nullable=True,
        default=None,
        comment="Ссылка на Telegram",
    ),
    Column(
        "telegram_id",
        Integer,
        nullable=True,
        default=None,
        comment="Идентификатор телеграма",
    ),
    Column(
        "vk", String(128), nullable=True, default=None, comment="Ссылка на VK"
    ),
    Column(
        "phone_number",
        String(32),
        nullable=True,
        default=None,
        comment="Номер телефона",
    ),
    Column(
        "email",
        String(128),
        index=True,
        nullable=False,
        comment="Адрес электронной почты",
    ),
    Column(
        "password",
        String(512),
        nullable=False,
        comment="Пароль",
    ),
    Column(
        "version",
        BigInteger,
        default=0,
        nullable=False,
        comment="Версия записи об объекте",
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="Дата и время, когда была создана запись",
    ),
    comment="Пользователи",
)

users_voted_events = Table(
    "users_voted_events",
    metadata,
    Column(
        "user_id",
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
        comment="Идентификатор пользователя",
    ),
    Column(
        "event_id",
        ForeignKey("events.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
        comment="Идентификатор события",
    ),
    Column(
        "vote",
        Boolean,
        nullable=False,
        comment="Голос пользователя",
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="Дата и время, когда была создана запись",
    ),
    comment="Оцененные пользователями события (ассоциативная таблица)",
)

users_enrolled_in_events = Table(
    "users_enrolled_in_events",
    metadata,
    Column(
        "user_id",
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
        comment="Идентификатор пользователя",
    ),
    Column(
        "event_id",
        ForeignKey("events.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
        comment="Идентификатор события",
    ),
    comment="Пользователи, записавшиеся на события (ассоциативная таблица)",
)


events = Table(
    "events",
    metadata,
    Column(
        "id", Integer, primary_key=True, nullable=False, comment="Уникальный идентификатор"
    ),
    Column("title", String(256), nullable=False, comment="Название"),
    Column(
        "description",
        Text,
        nullable=True,
        default=None,
        comment="Описание мероприятия",
    ),
    Column(
        "cover_id",
        ForeignKey("covers.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
        comment="Идентификатор обложки мероприятия",
    ),
    Column("status", String(64), nullable=False, comment="Статус"),
    Column(
        "place_id",
        ForeignKey("places.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
        comment="Идентификатор аудитории",
    ),
    Column(
        "datetime",
        DateTime(timezone=True),
        index=True,
        nullable=False,
        comment="Дата и время начала мероприятия",
    ),
    Column(
        "dateend",
        DateTime(timezone=True),
        index=True,
        nullable=False,
        comment="Дата и время конца мероприятия",
    ),
    Column(
        "creator_id",
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="Идентификатор пользователя, создавшего мероприятие",
    ),
    Column(
        "voted_yes",
        Integer,
        nullable=False,
        default=0,
        comment="Количество пользователей, проголосовавших ЗА",
    ),
    Column(
        "voted_no",
        Integer,
        nullable=False,
        default=0,
        comment="Количество пользователей, проголосовавших ПРОТИВ",
    ),
    Column(
        "type_id",
        ForeignKey("event_types.id", ondelete="CASCADE"),
        nullable=False,
        comment="Идентификатор типа мероприятия",
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="Дата и время, когда была создана запись",
    ),
    comment="Мероприятия",
)

event_types = Table(
    "event_types",
    metadata,
    Column(
        "id", Integer, primary_key=True, comment="Уникальный идентификатор"
    ),
    Column("title", String(256), nullable=False, comment="Название"),
    Column(
        "description", Text, nullable=True, default=None, comment="Описание"
    ),
    Column(
        "version",
        Integer,
        default=0,
        nullable=False,
        comment="Версия записи об объекте",
    ),
    comment="Типы мероприятий",
)

institutions = Table(
    "institutions",
    metadata,
    Column(
        "id", Integer, primary_key=True, comment="Уникальный идентификатор"
    ),
    Column("title", String(256), nullable=False, comment="Название"),
    Column(
        "description", Text, nullable=True, default=None, comment="Описание"
    ),
    Column(
        "version",
        Integer,
        default=0,
        nullable=False,
        comment="Версия записи об объекте",
    ),
    comment="Организации (факультеты и институты)",
)


places = Table(
    "places",
    metadata,
    Column(
        "id", Integer, primary_key=True, comment="Уникальный идентификатор"
    ),
    Column("title", String(256), nullable=False, comment="Наименование"),
    Column("floor", Integer, nullable=True, comment="Этаж"),
    Column(
        "institution_id",
        ForeignKey("institutions.id", ondelete="CASCADE"),
        nullable=True,
        default=None,
        comment="Идентификатор факультета/института, к которому относится аудитория",
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="Дата и время, когда была создана запись",
    ),
    comment="Место проведения (аудитории и прочее)",
)

clubs = Table(
    "clubs",
    metadata,
    Column(
        "id", Integer, primary_key=True, comment="Уникальный идентификатор"
    ),
    Column("title", String(256), nullable=False, comment="Название"),
    Column("description", Text, nullable=False, comment="Описание"),
    Column(
        "telegram",
        String(256),
        nullable=True,
        default=None,
        comment="Telegram",
    ),
    Column("vk", String(256), nullable=True, default=None, comment="VK"),
    Column(
        "youtube", String(256), nullable=True, default=None, comment="YouTube"
    ),
    Column(
        "rutube", String(256), nullable=True, default=None, comment="Rutube"
    ),
    Column(
        "tiktok", String(256), nullable=True, default=None, comment="TikTok"
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="Дата и время, когда была создана запись",
    ),
    comment="Секции (кружки)",
)

covers = Table(
    "covers",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
        comment="Уникальный идентификатор",
    ),
    Column(
        "filename",
        String(128),
        nullable=False,
        comment="Имя файла",
    ),
    Column(
        "path",
        String(512),
        nullable=False,
        comment="Путь к файлу на диске",
    ),
    Column(
        "uploader_id",
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        comment="Идентификатор пользователя, загрузившего обложку",
    ),
)

users_favorite_clubs = Table(
    "users_favorite_clubs",
    metadata,
    Column(
        "user_id",
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
        comment="Идентификатор пользователя",
    ),
    Column(
        "club_id",
        ForeignKey("clubs.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
        comment="Идентификатор секции",
    ),
    comment="Пользователи, добавившие секцию в избранное",
)

