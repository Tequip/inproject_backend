"""update_project

Revision ID: 96ef6e165f76
Revises: adf27a6f5ac4
Create Date: 2022-11-04 13:18:02.198536

"""
from alembic import op
from sqlalchemy import Column, Integer, String, ForeignKey, Float


# revision identifiers, used by Alembic.
revision = '96ef6e165f76'
down_revision = 'adf27a6f5ac4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("a_project_member_order",
                    Column("project_id", Integer(), ForeignKey("entity.project.id")),
                    Column("role", String(200), nullable=False),
                    schema="entity")

    op.create_table("a_project_member_recommend",
                    Column("project_id", Integer(), ForeignKey("entity.project.id")),
                    Column("user_id", Integer(), ForeignKey("user.user.id")),
                    Column("fits", Float(), nullable=False),
                    schema="entity")


def downgrade() -> None:
    op.drop_table("a_project_member_order", schema="entity")
    op.drop_table("a_project_member_recommend", schema="entity")
