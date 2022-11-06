"""update_event

Revision ID: 987759afcc54
Revises: 175123a593d9
Create Date: 2022-10-28 18:58:18.251913

"""
from alembic import op
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, Float


# revision identifiers, used by Alembic.
revision = '987759afcc54'
down_revision = '175123a593d9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("event",
                    Column("id", Integer(), primary_key=True),
                    Column("title", Text(), nullable=False),
                    Column("owner_id", Integer(), ForeignKey("user.user.id")),
                    Column("about", Text(), nullable=False),
                    Column("short_about", Text(), nullable=False),
                    Column("title_photo", Text(), nullable=True),
                    Column("created", DateTime(), nullable=False),
                    Column("start_date", DateTime(), nullable=False),
                    Column("end_date", DateTime(), nullable=False),
                    schema="entity"
                    )

    op.create_table("a_event_location",
                    Column("event_id", Integer(), ForeignKey("entity.event.id")),
                    Column("location_id", Integer(), ForeignKey("entity.location.id")),
                    schema="entity"
                    )

    op.create_table("a_event_tag",
                    Column("event_id", Integer(), ForeignKey("entity.event.id")),
                    Column("tag_id", Integer(), ForeignKey("entity.tag.id")),
                    schema="entity"
                    )

    op.create_table("a_event_category",
                    Column("event_id", Integer(), ForeignKey("entity.event.id")),
                    Column("category_id", Integer(), ForeignKey("entity.category.id")),
                    schema="entity"
                    )

    op.create_table("a_event_relation",
                    Column("event_id", Integer(), ForeignKey("entity.event.id")),
                    Column("relation_event_id", Integer(), ForeignKey("entity.event.id")),
                    Column("similarity", Float(), nullable=False),
                    schema="entity"
                    )


def downgrade() -> None:
    op.drop_table("a_event_relation", schema="entity")
    op.drop_table("a_event_category", schema="entity")
    op.drop_table("a_event_tag", schema="entity")
    op.drop_table("a_event_location", schema="entity")
    op.drop_table("event", schema="entity")
