"""update_user

Revision ID: 3eb6c24f081a
Revises: f4941e35a784
Create Date: 2022-11-06 15:08:08.093384

"""
from alembic import op
from sqlalchemy import Column, Boolean, text


# revision identifiers, used by Alembic.
revision = '3eb6c24f081a'
down_revision = 'f4941e35a784'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("user", "user") as batch_op:
        batch_op.add_column(Column("is_admin", Boolean(), nullable=True, server_default=text("False")))
        batch_op.alter_column("first_name", nullable=True)
        batch_op.alter_column("last_name", nullable=True)


def downgrade() -> None:
    with op.batch_alter_table("user", "user") as batch_op:
        batch_op.drop_column("is_admin")
        batch_op.alter_column("first_name", nullable=False)
        batch_op.alter_column("last_name", nullable=False)
