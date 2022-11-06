"""create_project

Revision ID: 10c54ab179d0
Revises: b4f530c2804f
Create Date: 2022-10-15 19:57:29.765367

"""
from alembic import op
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean


# revision identifiers, used by Alembic.
revision = '10c54ab179d0'
down_revision = 'b4f530c2804f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('CREATE SCHEMA "entity"')
    op.create_table("project",
                    Column("id", Integer(), primary_key=True),
                    Column("name", String(50), nullable=False),
                    Column("creator_id", Integer(), ForeignKey("user.user.id")),
                    Column("about", String(200), nullable=False),
                    Column("short_about", String(100), nullable=True),
                    Column("title_photo", String(), nullable=True),
                    Column("created", DateTime(), nullable=True),
                    Column("deadline", DateTime(), nullable=False),
                    schema="entity"
                    )

    op.create_table("tag",
                    Column("id", Integer(), primary_key=True),
                    Column("name", String(50), nullable=False),
                    schema="entity"
                    )

    op.create_table("location",
                    Column("id", Integer(), primary_key=True),
                    Column("name", String(50), nullable=False),
                    schema="entity"
                    )

    op.create_table("a_project_user",
                    Column("project_id", Integer(), ForeignKey("entity.project.id")),
                    Column("user_id", Integer(), ForeignKey("user.user.id")),
                    Column("member", Boolean()),
                    Column("like", Boolean()),
                    schema="entity"
                    )

    op.create_table("a_project_location",
                    Column("project_id", Integer(), ForeignKey("entity.project.id")),
                    Column("location_id", Integer(), ForeignKey("entity.location.id")),
                    schema="entity"
                    )

    op.create_table("a_project_tag",
                    Column("project_id", Integer(), ForeignKey("entity.project.id")),
                    Column("tag_id", Integer(), ForeignKey("entity.tag.id")),
                    schema="entity"
                    )


def downgrade() -> None:
    op.drop_table("a_project_tag", schema="entity")
    op.drop_table("a_project_location", schema="entity")
    op.drop_table("a_project_user", schema="entity")
    op.drop_table("location", schema="entity")
    op.drop_table("tag", schema="entity")
    op.drop_table("project", schema="entity")
    op.execute('DROP SCHEMA "entity"')
