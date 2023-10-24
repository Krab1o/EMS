"""Add user password

Revision ID: 6d340170026e
Revises: 88ba735f023c
Create Date: 2023-10-23 10:39:32.359950+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d340170026e'
down_revision = '88ba735f023c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('password', sa.String(length=512), nullable=False, comment='Пароль'))


def downgrade():
    op.drop_column('users', 'password')
