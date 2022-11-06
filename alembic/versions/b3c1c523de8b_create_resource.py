"""create_resource

Revision ID: b3c1c523de8b
Revises: 883f7da09a9c
Create Date: 2022-10-30 13:13:50.624547

"""
from alembic import op
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


# revision identifiers, used by Alembic.
revision = 'b3c1c523de8b'
down_revision = '883f7da09a9c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('CREATE SCHEMA "resource"')

    op.create_table("type",
                    Column("id", Integer(), primary_key=True),
                    Column("name", String(100), nullable=False),
                    schema="resource"
                    )

    op.create_table("extension",
                    Column("id", Integer(), primary_key=True),
                    Column("name", String(100), nullable=False),
                    Column("mn", String(10), nullable=False),
                    Column("media_type", String(100), nullable=False),
                    schema="resource"
                    )

    op.create_table("a_type_extension",
                    Column("type_id", Integer(), ForeignKey("resource.type.id")),
                    Column("extension_id", Integer(), ForeignKey("resource.extension.id")),
                    schema="resource"
                    )

    op.create_table("resource",
                    Column("id", Integer(), primary_key=True),
                    Column("path", String(100), nullable=False),
                    Column("original_name", String(255), nullable=False),
                    Column("extension_id", Integer(), ForeignKey("resource.extension.id")),
                    schema="resource"
                    )

    op.create_table("a_resource_project",
                    Column("resource_id", Integer(), ForeignKey("resource.resource.id")),
                    Column("project_id", Integer(), ForeignKey("entity.project.id")),
                    schema="resource")

    op.create_table("a_resource_event",
                    Column("resource_id", Integer(), ForeignKey("resource.resource.id")),
                    Column("event_id", Integer(), ForeignKey("entity.event.id")),
                    schema="resource")


def downgrade() -> None:
    op.drop_table("a_resource_project", schema="resource")
    op.drop_table("a_resource_event", schema="resource")
    op.drop_table("resource", schema="resource")
    op.drop_table("a_type_extension", schema="resource")
    op.drop_table("extension", schema="resource")
    op.drop_table("type", schema="resource")
    op.execute('DROP SCHEMA "resource"')
