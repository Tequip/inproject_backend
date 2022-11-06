"""update_project

Revision ID: 883f7da09a9c
Revises: 987759afcc54
Create Date: 2022-10-29 15:08:07.911287

"""
from alembic import op
from sqlalchemy import Column, Integer, String, ForeignKey


# revision identifiers, used by Alembic.
revision = '883f7da09a9c'
down_revision = '987759afcc54'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("stage",
                    Column("id", Integer(), primary_key=True),
                    Column("name", String(200), nullable=False),
                    schema="entity")

    with op.batch_alter_table("project", "entity") as batch_op:
        batch_op.add_column(Column("stage_id", Integer(), ForeignKey("entity.stage.id")))


def downgrade() -> None:
    with op.batch_alter_table("project", "entity") as batch_op:
        batch_op.drop_column("stage_id")

    op.drop_table("stage", schema="entity")
