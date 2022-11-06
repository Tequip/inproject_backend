"""user table change

Revision ID: b4f530c2804f
Revises: 8caf5d2669d9
Create Date: 2022-10-14 19:51:15.481339

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'b4f530c2804f'
down_revision = '8caf5d2669d9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("user", "user") as batch_op:
        batch_op.alter_column("role", nullable=True)


def downgrade() -> None:
    with op.batch_alter_table("user", "user") as batch_op:
        batch_op.alter_column("role", nullable=False)
