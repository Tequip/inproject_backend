"""create_audit

Revision ID: 48f2f52807aa
Revises: 09b9996c6ad3
Create Date: 2022-10-27 11:40:32.213847

"""
from alembic import op
from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, Text

# revision identifiers, used by Alembic.
revision = '48f2f52807aa'
down_revision = '09b9996c6ad3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('CREATE SCHEMA "audit"')
    op.create_table("audit",
                    Column("ts", DateTime(), primary_key=True, nullable=False),
                    Column("user_id", Integer(), ForeignKey("user.user.id"), primary_key=True, nullable=False),
                    Column("method", String(100), nullable=False),
                    Column("url", Text(), nullable=False),
                    Column("agent", Text()),
                    Column("params", Text),
                    schema="audit"
                    )

    op.execute("SELECT create_hypertable('audit.audit', 'ts');")


def downgrade() -> None:
    op.drop_table('audit', schema="audit")
    op.execute('DROP SCHEMA "audit"')
