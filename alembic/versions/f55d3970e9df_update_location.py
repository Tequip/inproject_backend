"""update_location

Revision ID: f55d3970e9df
Revises: 48f2f52807aa
Create Date: 2022-10-28 18:09:29.446464

"""
from alembic import op
from sqlalchemy import Column, String


# revision identifiers, used by Alembic.
revision = 'f55d3970e9df'
down_revision = '48f2f52807aa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("location", "entity") as batch_op:
        batch_op.add_column(Column("iso", String(50), nullable=False))


def downgrade() -> None:
    with op.batch_alter_table("location", "entity") as batch_op:
        batch_op.drop_column("iso")
