"""Fix ordering after update

Revision ID: c02ac222320d
Revises: e9bf9acf9cc0
Create Date: 2024-04-13 06:48:24.355923+00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c02ac222320d'
# down_revision = 'e9bf9acf9cc0'
down_revision = '3e3eaf2a7333'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('clubs', sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, comment='Дата и время, когда была создана запись'))
    op.create_index(op.f('ix_clubs_created_at'), 'clubs', ['created_at'], unique=False)
    op.create_index(op.f('ix_events_created_at'), 'events', ['created_at'], unique=False)
    op.add_column('users', sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, comment='Дата и время, когда была создана запись'))
    op.create_index(op.f('ix_users_created_at'), 'users', ['created_at'], unique=False)
    op.alter_column('users_voted_events', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment='Дата и время, когда была создана запись',
               existing_comment='Время создания записи',
               existing_nullable=False)
    op.create_index(op.f('ix_users_voted_events_created_at'), 'users_voted_events', ['created_at'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_users_voted_events_created_at'), table_name='users_voted_events')
    op.alter_column('users_voted_events', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment='Время создания записи',
               existing_comment='Дата и время, когда была создана запись',
               existing_nullable=False)
    op.drop_index(op.f('ix_users_created_at'), table_name='users')
    op.drop_column('users', 'created_at')
    op.drop_index(op.f('ix_events_created_at'), table_name='events')
    op.drop_index(op.f('ix_clubs_created_at'), table_name='clubs')
    op.drop_column('clubs', 'created_at')
