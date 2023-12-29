"""Remove event version

Revision ID: d9cb568e7ef6
Revises: a404a0f884f0
Create Date: 2023-12-29 14:37:08.509427+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9cb568e7ef6'
down_revision = 'a404a0f884f0'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('events', 'version')


def downgrade():
    op.add_column('events', sa.Column('version', sa.INTEGER(), autoincrement=False, nullable=False, comment='Версия записи об объекте'))
