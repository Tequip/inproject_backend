"""add_relation_project

Revision ID: e23022f19f8f
Revises: 354c81d4c2a1
Create Date: 2022-10-24 21:28:53.687993

"""
from alembic import op
from sqlalchemy import Column, Integer, ForeignKey, Float


# revision identifiers, used by Alembic.
revision = 'e23022f19f8f'
down_revision = '354c81d4c2a1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("a_project_relation",
                    Column("project_id", Integer(), ForeignKey("entity.project.id")),
                    Column("relation_project_id", Integer(), ForeignKey("entity.project.id")),
                    Column("score", Float(), nullable=False),
                    schema="entity")


def downgrade() -> None:
    op.drop_table('a_project_relation', schema="entity")
