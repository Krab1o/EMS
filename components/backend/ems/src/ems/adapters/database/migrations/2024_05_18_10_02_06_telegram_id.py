"""Telegram ID

Revision ID: 9daf2f38973b
Revises: aabf0a61d830
Create Date: 2024-05-18 10:02:06.223532+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9daf2f38973b'
down_revision = 'aabf0a61d830'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('telegram_id', sa.Integer(), nullable=True, comment='Идентификатор телеграма'))


def downgrade():
    op.drop_column('users', 'telegram_id')
