"""Event places

Revision ID: 2598b8ffc54a
Revises: e9bf9acf9cc0
Create Date: 2024-04-19 17:15:41.175471+00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2598b8ffc54a'
down_revision = 'c02ac222320d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('places',
    sa.Column('id', sa.Integer(), nullable=False, comment='Уникальный идентификатор'),
    sa.Column('title', sa.String(length=256), nullable=False, comment='Наименование'),
    sa.Column('floor', sa.Integer(), nullable=True, comment='Этаж'),
    sa.Column('institution_id', sa.Integer(), nullable=True, comment='Идентификатор факультета/института, к которому относится аудитория'),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, comment='Дата и время, когда была создана запись'),
    sa.ForeignKeyConstraint(['institution_id'], ['institutions.id'], name=op.f('fk_places_institution_id_institutions'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_places')),
    comment='Место проведения (аудитории и прочее)'
    )
    op.create_index(op.f('ix_places_created_at'), 'places', ['created_at'], unique=False)
    op.add_column('events', sa.Column('place_id', sa.Integer(), nullable=False, comment='Идентификатор аудитории'))
    op.add_column('events', sa.Column('dateend', sa.DateTime(timezone=True), nullable=False, comment='Дата и время конца мероприятия'))
    op.alter_column('events', 'datetime',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment='Дата и время начала мероприятия',
               existing_comment='Дата и время проведения',
               existing_nullable=False)
    op.create_index(op.f('ix_events_dateend'), 'events', ['dateend'], unique=False)
    op.create_foreign_key(op.f('fk_events_place_id_places'), 'events', 'places', ['place_id'], ['id'], ondelete='CASCADE')
    op.drop_column('events', 'place')


def downgrade():
    op.add_column('events', sa.Column('place', sa.VARCHAR(length=1024), autoincrement=False, nullable=False, comment='Место проведения'))
    op.drop_constraint(op.f('fk_events_place_id_places'), 'events', type_='foreignkey')
    op.drop_index(op.f('ix_events_dateend'), table_name='events')
    op.alter_column('events', 'datetime',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment='Дата и время проведения',
               existing_comment='Дата и время начала мероприятия',
               existing_nullable=False)
    op.drop_column('events', 'dateend')
    op.drop_column('events', 'place_id')
    op.drop_index(op.f('ix_places_created_at'), table_name='places')
    op.drop_table('places')
