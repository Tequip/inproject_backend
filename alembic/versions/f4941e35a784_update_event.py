"""update_event

Revision ID: f4941e35a784
Revises: ff6e4e3eb223
Create Date: 2022-11-06 14:03:36.869962

"""
from alembic import op
from sqlalchemy import Column, Text


# revision identifiers, used by Alembic.
revision = 'f4941e35a784'
down_revision = 'ff6e4e3eb223'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("event", "entity") as batch_op:
        batch_op.add_column(Column("source_url", Text(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("event", "entity") as batch_op:
        batch_op.drop_column("source_url")
