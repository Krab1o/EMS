"""Add user liked event fields

Revision ID: 3a12be09415f
Revises: 24c80e16cd81
Create Date: 2023-12-02 16:06:10.954850+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a12be09415f'
down_revision = '24c80e16cd81'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users_voted_events',
        sa.Column('user_id', sa.Integer(), nullable=False, comment='Идентификатор пользователя'),
        sa.Column('event_id', sa.Integer(), nullable=False, comment='Идентификатор события'),
        sa.Column('vote', sa.Boolean(), nullable=False, comment='Голос пользователя'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, comment='Время создания записи'),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], name=op.f('fk_users_voted_events_event_id_events'), ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_users_voted_events_user_id_users'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'event_id', name=op.f('pk_users_voted_events')),
        comment='Оцененные пользователями события (ассоциативная таблица)'
    )
    op.drop_table('users_liked_events')


def downgrade():
    op.create_table('users_liked_events',
        sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False, comment='Идентификатор пользователя'),
        sa.Column('event_id', sa.INTEGER(), autoincrement=False, nullable=False, comment='Идентификатор события'),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], name='fk_users_liked_events_event_id_events', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_users_liked_events_user_id_users', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'event_id', name='pk_users_liked_events'),
        comment='Лайкнутые пользователями события (ассоциативная таблица)'
    )
    op.drop_table('users_voted_events')
