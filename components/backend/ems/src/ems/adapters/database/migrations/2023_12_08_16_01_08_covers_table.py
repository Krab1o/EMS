"""covers table

Revision ID: d0a6403d31ef
Revises: 3a12be09415f
Create Date: 2023-12-08 16:01:08.464920+00:00

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d0a6403d31ef"
down_revision = "3a12be09415f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "covers",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
            comment="Уникальный идентификатор",
        ),
        sa.Column(
            "filename",
            sa.String(length=128),
            nullable=False,
            comment="Имя файла",
        ),
        sa.Column(
            "path",
            sa.String(length=512),
            nullable=False,
            comment="Путь к файлу на диске",
        ),
        sa.Column(
            "uploader_id",
            sa.Integer(),
            nullable=True,
            comment="Идентификатор пользователя, загрузившего обложку",
        ),
        sa.ForeignKeyConstraint(
            ["uploader_id"],
            ["users.id"],
            name=op.f("fk_covers_uploader_id_users"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_covers")),
    )
    op.add_column(
        "events",
        sa.Column(
            "cover_id",
            sa.Integer(),
            nullable=True,
            comment="Идентификатор обложки мероприятия",
        ),
    )
    op.drop_column("events", "cover")


def downgrade():
    op.add_column(
        "events",
        sa.Column(
            "cover",
            sa.VARCHAR(length=256),
            autoincrement=False,
            nullable=True,
            comment="URI обложки мероприятия",
        ),
    )
    op.drop_column("events", "cover_id")
    op.drop_table("covers")
