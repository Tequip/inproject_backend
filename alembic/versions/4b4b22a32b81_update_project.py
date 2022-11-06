"""update_project

Revision ID: 4b4b22a32b81
Revises: c57cfd7668be
Create Date: 2022-10-31 13:20:39.997989

"""
from alembic import op
from sqlalchemy import Column, Boolean


# revision identifiers, used by Alembic.
revision = '4b4b22a32b81'
down_revision = 'c57cfd7668be'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("project", "entity") as batch_op:
        batch_op.add_column(Column("is_hidden", Boolean(), nullable=True, server_default="False"))


def downgrade() -> None:
    with op.batch_alter_table("project", "entity") as batch_op:
        batch_op.drop_column("is_hidden")
