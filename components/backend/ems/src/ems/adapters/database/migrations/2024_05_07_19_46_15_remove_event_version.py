"""Remove event version

Revision ID: 2da3d92a1fba
Revises: e9bf9acf9cc0
Create Date: 2024-05-07 19:46:15.572948+00:00

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '2da3d92a1fba'
down_revision = 'e9bf9acf9cc0'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('events', 'version')


def downgrade():
    op.add_column('events', sa.Column('version', sa.INTEGER(), autoincrement=False, nullable=False, comment='Версия записи об объекте'))
