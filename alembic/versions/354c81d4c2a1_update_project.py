"""update_project

Revision ID: 354c81d4c2a1
Revises: 10c54ab179d0
Create Date: 2022-10-18 19:44:59.262545

"""
from alembic import op
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime


# revision identifiers, used by Alembic.
revision = '354c81d4c2a1'
down_revision = '10c54ab179d0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("project", "entity") as batch_op:
        batch_op.alter_column("name", new_column_name="title")
        batch_op.alter_column("creator_id", new_column_name="owner_id")
        batch_op.alter_column("short_about", nullable=False)
        batch_op.alter_column("created", nullable=False)
        batch_op.alter_column("deadline", nullable=True)
        batch_op.add_column(Column("likes", Integer(), nullable=True))

    op.drop_table("a_project_user", schema="entity")

    op.create_table("a_project_member",
                    Column("project_id", Integer(), ForeignKey("entity.project.id")),
                    Column("member_id", Integer(), ForeignKey("user.user.id")),
                    Column("active", Boolean(), nullable=False),
                    Column("joined", DateTime(), nullable=False),
                    Column("removed", DateTime(), nullable=True),
                    Column("role", String(100), nullable=False),
                    schema="entity")

    op.create_table("a_project_like",
                    Column("project_id", Integer(), ForeignKey("entity.project.id")),
                    Column("user_id", Integer(), ForeignKey("user.user.id")),
                    Column("datetime", DateTime(), nullable=False),
                    schema="entity")

    op.create_table("category",
                    Column("id", Integer(), primary_key=True),
                    Column("name", String(50), nullable=False),
                    schema="entity")

    op.create_table("a_project_category",
                    Column("project_id", Integer(), ForeignKey("entity.project.id")),
                    Column("category_id", Integer(), ForeignKey("entity.category.id")),
                    schema="entity")


def downgrade() -> None:
    with op.batch_alter_table("project", "entity") as batch_op:
        batch_op.alter_column("title", new_column_name="name")
        batch_op.alter_column("owner_id", new_column_name="creator_id")
        batch_op.alter_column("short_about", nullable=True)
        batch_op.alter_column("created", nullable=True)
        batch_op.alter_column("deadline", nullable=False)
        batch_op.drop_column("likes")

    op.drop_table("a_project_member", schema="entity")

    op.create_table("a_project_user",
                    Column("project_id", Integer(), ForeignKey("entity.project.id")),
                    Column("user_id", Integer(), ForeignKey("user.user.id")),
                    Column("member", Boolean()),
                    Column("like", Boolean()),
                    schema="entity")

    op.drop_table("a_project_like", schema="entity")
    op.drop_table("category", schema="entity")
    op.drop_table("a_project_category", schema="entity")
