"""update_resource

Revision ID: 9b5dd8a714e1
Revises: f43e80cdaf6c
Create Date: 2022-11-02 17:40:40.089366

"""
from alembic import op
from sqlalchemy import Column, Integer, ForeignKey


# revision identifiers, used by Alembic.
revision = '9b5dd8a714e1'
down_revision = 'f43e80cdaf6c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("a_image_project",
                    Column("resource_id", Integer(), ForeignKey("resource.resource.id")),
                    Column("project_id", Integer(), ForeignKey("entity.project.id")),
                    schema="resource"
                    )

    op.create_table("a_image_event",
                    Column("resource_id", Integer(), ForeignKey("resource.resource.id")),
                    Column("event_id", Integer(), ForeignKey("entity.event.id")),
                    schema="resource"
                    )

    op.create_table("a_image_user",
                    Column("resource_id", Integer(), ForeignKey("resource.resource.id")),
                    Column("user_id", Integer(), ForeignKey("user.user.id")),
                    schema="resource"
                    )


def downgrade() -> None:
    op.drop_table("a_image_project", schema="resource")
    op.drop_table("a_image_event", schema="resource")
    op.drop_table("a_image_user", schema="resource")
