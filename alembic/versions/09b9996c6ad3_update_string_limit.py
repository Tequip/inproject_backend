"""update_string_limit

Revision ID: 09b9996c6ad3
Revises: e23022f19f8f
Create Date: 2022-10-25 18:33:42.037842

"""
from alembic import op
from sqlalchemy import String, Text


# revision identifiers, used by Alembic.
revision = '09b9996c6ad3'
down_revision = 'e23022f19f8f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("category", "entity") as batch_op:
        batch_op.alter_column("name", type_=String(200))

    with op.batch_alter_table("location", "entity") as batch_op:
        batch_op.alter_column("name", type_=String(200))

    with op.batch_alter_table("tag", "entity") as batch_op:
        batch_op.alter_column("name", type_=String(200))

    with op.batch_alter_table("a_project_member", "entity") as batch_op:
        batch_op.alter_column("role", type_=String(200))

    with op.batch_alter_table("project", "entity") as batch_op:
        batch_op.alter_column("title", type_=Text())
        batch_op.alter_column("about", type_=Text())
        batch_op.alter_column("short_about", type_=Text())

    with op.batch_alter_table("skill", "user") as batch_op:
        batch_op.alter_column("name", type_=String(200))

    with op.batch_alter_table("interest", "user") as batch_op:
        batch_op.alter_column("name", type_=String(200))

    with op.batch_alter_table("auth", "user") as batch_op:
        batch_op.alter_column("password_hash", type_=String(400))

    with op.batch_alter_table("update_token_white_list", "user") as batch_op:
        batch_op.alter_column("update_token", type_=String(400))

    with op.batch_alter_table("user", "user") as batch_op:
        batch_op.alter_column("first_name", type_=String(100))
        batch_op.alter_column("last_name", type_=String(100))
        batch_op.alter_column("email", type_=String(300))
        batch_op.alter_column("telegram", type_=String(100))
        batch_op.alter_column("status", type_=String(300))
        batch_op.alter_column("role", type_=String(300))


def downgrade() -> None:
    with op.batch_alter_table("category", "entity") as batch_op:
        batch_op.alter_column("name", type_=String(50))

    with op.batch_alter_table("location", "entity") as batch_op:
        batch_op.alter_column("name", type_=String(50))

    with op.batch_alter_table("tag", "entity") as batch_op:
        batch_op.alter_column("name", type_=String(50))

    with op.batch_alter_table("a_project_member", "entity") as batch_op:
        batch_op.alter_column("role", type_=String(100))

    with op.batch_alter_table("project", "entity") as batch_op:
        batch_op.alter_column("title", type_=String(50))
        batch_op.alter_column("about", type_=String(200))
        batch_op.alter_column("short_about", type_=String(100))

    with op.batch_alter_table("skill", "user") as batch_op:
        batch_op.alter_column("name", type_=String(50))

    with op.batch_alter_table("interest", "user") as batch_op:
        batch_op.alter_column("name", type_=String(50))

    with op.batch_alter_table("auth", "user") as batch_op:
        batch_op.alter_column("password_hash", type_=String(200))

    with op.batch_alter_table("update_token_white_list", "user") as batch_op:
        batch_op.alter_column("update_token", type_=String(200))

    with op.batch_alter_table("user", "user") as batch_op:
        batch_op.alter_column("first_name", type_=String(50))
        batch_op.alter_column("last_name", type_=String(50))
        batch_op.alter_column("email", type_=String(200))
        batch_op.alter_column("telegram", type_=String(50))
        batch_op.alter_column("status", type_=String(50))
        batch_op.alter_column("role", type_=String(50))
