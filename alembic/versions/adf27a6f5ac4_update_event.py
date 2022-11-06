"""update_event

Revision ID: adf27a6f5ac4
Revises: 9b5dd8a714e1
Create Date: 2022-11-04 11:57:21.346999

"""
from alembic import op
from sqlalchemy import Column, Boolean, text


# revision identifiers, used by Alembic.
revision = 'adf27a6f5ac4'
down_revision = '9b5dd8a714e1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("event", "entity") as batch_op:
        batch_op.add_column(Column("is_hidden", Boolean(), nullable=True, server_default=text("False")))
        batch_op.alter_column("created", server_default=text("now()"))

    with op.batch_alter_table("a_event_location", "entity") as batch_op:
        batch_op.create_unique_constraint("uq_event_location", ["event_id", "location_id"])

    with op.batch_alter_table("a_event_tag", "entity") as batch_op:
        batch_op.create_unique_constraint("uq_event_tag", ["event_id", "tag_id"])

    with op.batch_alter_table("a_event_category", "entity") as batch_op:
        batch_op.create_unique_constraint("uq_event_category", ["event_id", "category_id"])

    with op.batch_alter_table("a_event_relation", "entity") as batch_op:
        batch_op.create_unique_constraint("uq_event_relation_event", ["event_id", "relation_event_id"])


def downgrade() -> None:
    with op.batch_alter_table("event", "entity") as batch_op:
        batch_op.alter_column("created", server_default=None)
        batch_op.drop_column("is_hidden")

    with op.batch_alter_table("a_event_location", "entity") as batch_op:
        batch_op.drop_constraint("uq_event_location")

    with op.batch_alter_table("a_event_tag", "entity") as batch_op:
        batch_op.drop_constraint("uq_event_tag")

    with op.batch_alter_table("a_event_category", "entity") as batch_op:
        batch_op.drop_constraint("uq_event_category")

    with op.batch_alter_table("a_event_relation", "entity") as batch_op:
        batch_op.drop_constraint("uq_event_relation_event")
