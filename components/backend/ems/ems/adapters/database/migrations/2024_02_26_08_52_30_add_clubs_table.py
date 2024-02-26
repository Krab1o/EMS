"""add clubs table

Revision ID: 3e3eaf2a7333
Revises: a404a0f884f0
Create Date: 2024-02-26 08:52:30.839767+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e3eaf2a7333'
down_revision = 'a404a0f884f0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users_favorite_clubs',
    sa.Column('user_id', sa.Integer(), nullable=False, comment='Идентификатор пользователя'),
    sa.Column('club_id', sa.Integer(), nullable=False, comment='Идентификатор секции'),
    sa.ForeignKeyConstraint(['club_id'], ['clubs.id'], name=op.f('fk_users_favorite_clubs_club_id_clubs'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_users_favorite_clubs_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'club_id', name=op.f('pk_users_favorite_clubs')),
    comment='Пользователи, добавившие секцию в избранное'
    )
    op.add_column('clubs', sa.Column('telegram', sa.String(length=256), nullable=True, comment='Telegram'))
    op.add_column('clubs', sa.Column('vk', sa.String(length=256), nullable=True, comment='VK'))
    op.add_column('clubs', sa.Column('youtube', sa.String(length=256), nullable=True, comment='YouTube'))
    op.add_column('clubs', sa.Column('rutube', sa.String(length=256), nullable=True, comment='Rutube'))
    op.add_column('clubs', sa.Column('tiktok', sa.String(length=256), nullable=True, comment='TikTok'))
    op.alter_column('clubs', 'description',
               existing_type=sa.TEXT(),
               nullable=False,
               existing_comment='Описание')
    op.drop_column('clubs', 'place')
    op.drop_column('clubs', 'version')


def downgrade():
    op.add_column('clubs', sa.Column('version', sa.INTEGER(), autoincrement=False, nullable=False, comment='Версия записи об объекте'))
    op.add_column('clubs', sa.Column('place', sa.VARCHAR(length=512), autoincrement=False, nullable=False, comment='Место проведения'))
    op.alter_column('clubs', 'description',
               existing_type=sa.TEXT(),
               nullable=True,
               existing_comment='Описание')
    op.drop_column('clubs', 'tiktok')
    op.drop_column('clubs', 'rutube')
    op.drop_column('clubs', 'youtube')
    op.drop_column('clubs', 'vk')
    op.drop_column('clubs', 'telegram')
    op.drop_table('users_favorite_clubs')
