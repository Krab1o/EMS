"""Optional institution

Revision ID: aabf0a61d830
Revises: 2da3d92a1fba
Create Date: 2024-05-17 20:48:38.868043+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aabf0a61d830'
down_revision = '2da3d92a1fba'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('users', 'institution_id',
               existing_type=sa.INTEGER(),
               nullable=True,
               existing_comment='Идентификатор факультета/института, к которому относится пользователь')
    op.drop_constraint('fk_users_institution_id_institutions', 'users', type_='foreignkey')
    op.create_foreign_key(op.f('fk_users_institution_id_institutions'), 'users', 'institutions', ['institution_id'], ['id'], ondelete='SET NULL')


def downgrade():
    op.drop_constraint(op.f('fk_users_institution_id_institutions'), 'users', type_='foreignkey')
    op.create_foreign_key('fk_users_institution_id_institutions', 'users', 'institutions', ['institution_id'], ['id'], ondelete='CASCADE')
    op.alter_column('users', 'institution_id',
               existing_type=sa.INTEGER(),
               nullable=False,
               existing_comment='Идентификатор факультета/института, к которому относится пользователь')
