"""update_user

Revision ID: 175123a593d9
Revises: f55d3970e9df
Create Date: 2022-10-28 18:45:00.136273

"""
from alembic import op
from sqlalchemy import Column, DateTime


# revision identifiers, used by Alembic.
revision = '175123a593d9'
down_revision = 'f55d3970e9df'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("user", "user") as batch_op:
        batch_op.add_column(Column("birthday", DateTime(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("user", "user") as batch_op:
        batch_op.drop_column("birthday")
