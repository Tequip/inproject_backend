"""Create auth

Revision ID: 8caf5d2669d9
Revises: 74439c274036
Create Date: 2022-10-08 19:45:49.516175

"""
from alembic import op
from sqlalchemy import Column, Integer, String, ForeignKey


# revision identifiers, used by Alembic.
revision = '8caf5d2669d9'
down_revision = '74439c274036'
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "auth",
        Column("user_id", Integer(), ForeignKey("user.user.id"), primary_key=True),
        Column("password_hash", String(200), nullable=False),
        schema="user"
    )

    op.create_table(
        "update_token_white_list",
        Column("user_id", Integer(), ForeignKey("user.user.id")),
        Column("update_token", String(200), nullable=False),
        schema="user"
    )


def downgrade() -> None:
    op.drop_table("auth", schema="user")
    op.drop_table("update_token_white_list", schema="user")
