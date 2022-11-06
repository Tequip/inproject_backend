"""update_project

Revision ID: b6c20a5d5134
Revises: 498241fe2ba3
Create Date: 2022-11-04 16:40:58.516914

"""
from alembic import op
from sqlalchemy import Column, Integer, Float, ForeignKey


# revision identifiers, used by Alembic.
revision = 'b6c20a5d5134'
down_revision = '498241fe2ba3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("a_project_category_predict",
                    Column("project_id", Integer(), ForeignKey("entity.project.id")),
                    Column("category_id", Integer(), ForeignKey("entity.category.id")),
                    Column("similarity", Float(), nullable=False),
                    schema="entity")


def downgrade() -> None:
    op.drop_table("a_project_category_predict", schema="entity")
