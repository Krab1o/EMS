"""Timezone-aware datetimes

Revision ID: a404a0f884f0
Revises: d0a6403d31ef
Create Date: 2023-12-08 17:07:46.537629+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a404a0f884f0'
down_revision = 'd0a6403d31ef'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key(op.f('fk_events_cover_id_covers'), 'events', 'covers', ['cover_id'], ['id'], ondelete='SET NULL')


def downgrade():
    op.drop_constraint(op.f('fk_events_cover_id_covers'), 'events', type_='foreignkey')
