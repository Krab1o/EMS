"""Init schema

Revision ID: 88ba735f023c
Revises: 
Create Date: 2023-10-13 17:17:42.511875+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88ba735f023c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'clubs',
        sa.Column('id', sa.Integer(), nullable=False, comment='Уникальный идентификатор'),
        sa.Column('title', sa.String(length=256), nullable=False, comment='Название'),
        sa.Column('description', sa.Text(), nullable=True, comment='Описание'),
        sa.Column('place', sa.String(length=512), nullable=False, comment='Место проведения'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_clubs')),
        comment='Секции (кружки)'
    )
    op.create_table(
        'event_types',
        sa.Column('id', sa.Integer(), nullable=False, comment='Уникальный идентификатор'),
        sa.Column('title', sa.String(length=256), nullable=False, comment='Название'),
        sa.Column('description', sa.Text(), nullable=True, comment='Описание'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_event_types')),
        comment='Типы мероприятий'
    )
    op.create_table(
        'institutions',
        sa.Column('id', sa.Integer(), nullable=False, comment='Уникальный идентификатор'),
        sa.Column('title', sa.String(length=256), nullable=False, comment='Название'),
        sa.Column('description', sa.Text(), nullable=True, comment='Описание'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_institutions')),
        comment='Организации (факультеты и институты)'
    )
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False, comment='Уникальный идентификатор'),
        sa.Column('last_name', sa.String(length=128), nullable=False, comment='Фамилия'),
        sa.Column('first_name', sa.String(length=128), nullable=False, comment='Имя'),
        sa.Column('middle_name', sa.String(length=128), nullable=True, comment='Отчество'),
        sa.Column('institution_id', sa.Integer(), nullable=False, comment='Идентификатор факультета/института, к которому относится пользователь'),
        sa.Column('course', sa.Integer(), nullable=True, comment='Номер курса'),
        sa.Column('group', sa.Integer(), nullable=True, comment='Номер группы'),
        sa.Column('role', sa.String(length=64), nullable=False, comment='Роль'),
        sa.Column('telegram', sa.String(length=128), nullable=True, comment='Ссылка на Telegram'),
        sa.Column('vk', sa.String(length=128), nullable=True, comment='Ссылка на VK'),
        sa.Column('phone_number', sa.String(length=32), nullable=True, comment='Номер телефона'),
        sa.Column('email', sa.String(length=128), nullable=False, comment='Адрес электронной почты'),
        sa.ForeignKeyConstraint(['institution_id'], ['institutions.id'], name=op.f('fk_users_institution_id_institutions'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
        comment='Пользователи'
    )
    op.create_table(
        'events',
        sa.Column('id', sa.Integer(), nullable=False, comment='Уникальный идентификатор'),
        sa.Column('title', sa.String(length=256), nullable=False, comment='Название'),
        sa.Column('description', sa.Text(), nullable=True, comment='Описание мероприятия'),
        sa.Column('cover', sa.String(length=256), nullable=True, comment='URI обложки мероприятия'),
        sa.Column('status', sa.String(length=64), nullable=False, comment='Статус'),
        sa.Column('place', sa.String(length=1024), nullable=False, comment='Место проведения'),
        sa.Column('datetime', sa.DateTime(), nullable=False, comment='Дата и время проведения'),
        sa.Column('creator_id', sa.Integer(), nullable=False, comment='Идентификатор пользователя, создавшего мероприятие'),
        sa.Column('voted_yes', sa.Integer(), nullable=False, comment='Количество пользователей, проголосовавших ЗА'),
        sa.Column('voted_no', sa.Integer(), nullable=False, comment='Количество пользователей, проголосовавших ПРОТИВ'),
        sa.Column('type_id', sa.Integer(), nullable=False, comment='Идентификатор типа мероприятия'),
        sa.ForeignKeyConstraint(['creator_id'], ['users.id'], name=op.f('fk_events_creator_id_users'), ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['type_id'], ['event_types.id'], name=op.f('fk_events_type_id_event_types'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_events')),
        comment='Мероприятия'
    )
    op.create_table(
        'users_enrolled_in_events',
        sa.Column('user_id', sa.Integer(), nullable=False, comment='Идентификатор пользователя'),
        sa.Column('event_id', sa.Integer(), nullable=False, comment='Идентификатор события'),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], name=op.f('fk_users_enrolled_in_events_event_id_events'), ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_users_enrolled_in_events_user_id_users'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'event_id', name=op.f('pk_users_enrolled_in_events')),
        comment='Пользователи, записавшиеся на события (ассоциативная таблица)'
    )
    op.create_table(
        'users_liked_events',
        sa.Column('user_id', sa.Integer(), nullable=False, comment='Идентификатор пользователя'),
        sa.Column('event_id', sa.Integer(), nullable=False, comment='Идентификатор события'),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], name=op.f('fk_users_liked_events_event_id_events'), ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_users_liked_events_user_id_users'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'event_id', name=op.f('pk_users_liked_events')),
        comment='Лайкнутые пользователями события (ассоциативная таблица)'
    )


def downgrade():
    op.drop_table('users_liked_events')
    op.drop_table('users_enrolled_in_events')
    op.drop_table('events')
    op.drop_table('users')
    op.drop_table('institutions')
    op.drop_table('event_types')
    op.drop_table('clubs')
