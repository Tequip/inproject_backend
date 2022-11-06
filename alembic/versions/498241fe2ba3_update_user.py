"""update_user

Revision ID: 498241fe2ba3
Revises: 96ef6e165f76
Create Date: 2022-11-04 15:59:04.305445

"""
from alembic import op
from sqlalchemy import Column, Boolean, DateTime, text


# revision identifiers, used by Alembic.
revision = '498241fe2ba3'
down_revision = '96ef6e165f76'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("user", "user") as batch_op:
        batch_op.add_column(Column("is_hidden", Boolean(), nullable=True, server_default=text("False")))
        batch_op.add_column(Column("created", DateTime(), nullable=False, server_default=text("now()")))


def downgrade() -> None:
    with op.batch_alter_table("user", "user") as batch_op:
        batch_op.drop_column("is_hidden")
        batch_op.drop_column("created")
