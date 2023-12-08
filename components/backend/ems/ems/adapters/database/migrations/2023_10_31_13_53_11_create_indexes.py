"""Create indexes

Revision ID: 24c80e16cd81
Revises: 6d340170026e
Create Date: 2023-10-31 13:53:11.267680+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24c80e16cd81'
down_revision = '6d340170026e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('clubs', sa.Column('version', sa.Integer(), nullable=False, comment='Версия записи об объекте'))
    op.add_column('event_types', sa.Column('version', sa.Integer(), nullable=False, comment='Версия записи об объекте'))
    op.add_column('events', sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, comment='Дата и время, когда была создана запись'))
    op.add_column('events', sa.Column('version', sa.Integer(), nullable=False, comment='Версия записи об объекте'))
    op.create_index(op.f('ix_events_datetime'), 'events', ['datetime'], unique=False)
    op.add_column('institutions', sa.Column('version', sa.Integer(), nullable=False, comment='Версия записи об объекте'))
    op.add_column('users', sa.Column('version', sa.Integer(), nullable=False, comment='Версия записи об объекте'))
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_column('users', 'version')
    op.drop_column('institutions', 'version')
    op.drop_index(op.f('ix_events_datetime'), table_name='events')
    op.drop_column('events', 'version')
    op.drop_column('events', 'created_at')
    op.drop_column('event_types', 'version')
    op.drop_column('clubs', 'version')
