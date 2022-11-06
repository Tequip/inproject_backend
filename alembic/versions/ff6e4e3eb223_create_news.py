"""create_news

Revision ID: ff6e4e3eb223
Revises: b6c20a5d5134
Create Date: 2022-11-05 13:13:55.733172

"""
from alembic import op
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, text


# revision identifiers, used by Alembic.
revision = 'ff6e4e3eb223'
down_revision = 'b6c20a5d5134'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("news",
                    Column("id", Integer(), primary_key=True),
                    Column("title", Text(), nullable=False),
                    Column("text", Text(), nullable=False),
                    Column("created", DateTime(), nullable=False, server_default=text("now()")),
                    Column("project_id", Integer(), ForeignKey("entity.project.id")),
                    schema="entity")


def downgrade() -> None:
    op.drop_table("news", schema="entity")
