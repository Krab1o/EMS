from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
)

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

metadata = MetaData(
    naming_convention=naming_convention
)

users = Table(
    'users',
    metadata,
    Column(
        'id',
        Integer,
        primary_key=True,
        comment='Уникальный идентификатор'
    ),
    Column(
        'last_name',
        String(128),
        nullable=False,
        comment='Фамилия'
    ),
    Column(
        'first_name',
        String(128),
        nullable=False,
        comment='Имя'
    ),
    Column(
        'middle_name',
        String(128),
        nullable=True,
        default=None,
        comment='Отчество'
    ),
    Column(
        'institution_id',
        ForeignKey('institutions.id', ondelete='CASCADE'),
        nullable=False,
        comment='Идентификатор факультета/института, к которому относится пользователь'
    ),
    Column(
        'course',
        Integer,
        nullable=True,
        default=None,
        comment='Номер курса'
    ),
    Column(
        'group',
        Integer,
        nullable=True,
        default=None,
        comment='Номер группы'
    ),
    Column(
        'role',
        String(64),
        nullable=False,
        comment='Роль'
    ),
    Column(
        'telegram',
        String(128),
        nullable=True,
        default=None,
        comment='Ссылка на Telegram'
    ),
    Column(
        'vk',
        String(128),
        nullable=True,
        default=None,
        comment='Ссылка на VK'
    ),
    Column(
        'phone_number',
        String(32),
        nullable=True,
        default=None,
        comment='Номер телефона'
    ),
    Column(
        'email',
        String(128),
        nullable=False,
        comment='Адрес электронной почты'
    ),
    Column(
        'password',
        String(512),
        nullable=False,
        comment='Пароль',
    ),
    comment='Пользователи',
)

users_liked_events = Table(
    'users_liked_events',
    metadata,
    Column(
        'user_id',
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True,
        nullable=False,
        comment='Идентификатор пользователя'
    ),
    Column(
        'event_id',
        ForeignKey('events.id', ondelete='CASCADE'),
        primary_key=True,
        nullable=False,
        comment='Идентификатор события'
    ),
    comment='Лайкнутые пользователями события (ассоциативная таблица)'
)

users_enrolled_in_events = Table(
    'users_enrolled_in_events',
    metadata,
    Column(
        'user_id',
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True,
        nullable=False,
        comment='Идентификатор пользователя'
    ),
    Column(
        'event_id',
        ForeignKey('events.id', ondelete='CASCADE'),
        primary_key=True,
        nullable=False,
        comment='Идентификатор события'
    ),
    comment='Пользователи, записавшиеся на события (ассоциативная таблица)'
)


events = Table(
    'events',
    metadata,
    Column(
        'id',
        Integer,
        primary_key=True,
        comment='Уникальный идентификатор'
    ),
    Column(
        'title',
        String(256),
        nullable=False,
        comment='Название'
    ),
    Column(
        'description',
        Text,
        nullable=True,
        default=None,
        comment='Описание мероприятия'
    ),
    Column(
        'cover',
        String(256),
        nullable=True,
        default=None,
        comment='URI обложки мероприятия'
    ),
    Column(
        'status',
        String(64),
        nullable=False,
        comment='Статус'
    ),
    Column(
        'place',
        String(1024),
        nullable=False,
        comment='Место проведения'
    ),
    Column(
        'datetime',
        DateTime,
        nullable=False,
        comment='Дата и время проведения'
    ),
    Column(
        'creator_id',
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        comment='Идентификатор пользователя, создавшего мероприятие'
    ),
    Column(
        'voted_yes',
        Integer,
        nullable=False,
        comment='Количество пользователей, проголосовавших ЗА'
    ),
    Column(
        'voted_no',
        Integer,
        nullable=False,
        comment='Количество пользователей, проголосовавших ПРОТИВ'
    ),
    Column(
        'type_id',
        ForeignKey('event_types.id', ondelete='CASCADE'),
        nullable=False,
        comment='Идентификатор типа мероприятия'
    ),
    comment='Мероприятия',
)

event_types = Table(
    'event_types',
    metadata,
    Column(
        'id',
        Integer,
        primary_key=True,
        comment='Уникальный идентификатор'
    ),
    Column(
        'title',
        String(256),
        nullable=False,
        comment='Название'
    ),
    Column(
        'description',
        Text,
        nullable=True,
        default=None,
        comment='Описание'
    ),
    comment='Типы мероприятий',
)

institutions = Table(
    'institutions',
    metadata,
    Column(
        'id',
        Integer,
        primary_key=True,
        comment='Уникальный идентификатор'
    ),
    Column(
        'title',
        String(256),
        nullable=False,
        comment='Название'
    ),
    Column(
        'description',
        Text,
        nullable=True,
        default=None,
        comment='Описание'
    ),
    comment='Организации (факультеты и институты)',
)

clubs = Table(
    'clubs',
    metadata,
    Column(
        'id',
        Integer,
        primary_key=True,
        comment='Уникальный идентификатор'
    ),
    Column(
        'title',
        String(256),
        nullable=False,
        comment='Название'
    ),
    Column(
        'description',
        Text,
        nullable=True,
        default=None,
        comment='Описание'
    ),
    Column(
        'place',
        String(512),
        nullable=False,
        comment='Место проведения'
    ),
    comment='Секции (кружки)',
)
