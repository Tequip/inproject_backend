"""update_project

Revision ID: c57cfd7668be
Revises: b3c1c523de8b
Create Date: 2022-10-31 11:41:30.861716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c57cfd7668be'
down_revision = 'b3c1c523de8b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("project", "entity") as batch_op:
        batch_op.alter_column("owner_id", nullable=False)
        batch_op.alter_column("likes", server_default='0')


def downgrade() -> None:
    with op.batch_alter_table("project", "entity") as batch_op:
        batch_op.alter_column("owner_id", nullable=True)
        batch_op.alter_column("likes", server_default=None)
