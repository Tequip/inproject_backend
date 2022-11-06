"""update_project

Revision ID: f43e80cdaf6c
Revises: 4b4b22a32b81
Create Date: 2022-11-01 09:51:44.086985

"""
from alembic import op
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = 'f43e80cdaf6c'
down_revision = '4b4b22a32b81'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("project", "entity") as batch_op:
        batch_op.alter_column("created", server_default=text('now()'))
        batch_op.drop_column("title_photo")

    with op.batch_alter_table("a_project_member", "entity") as batch_op:
        batch_op.alter_column("joined", server_default=text('now()'))
        batch_op.create_unique_constraint("uq_project_member", ["project_id", "member_id"])

    with op.batch_alter_table("a_project_like", "entity") as batch_op:
        batch_op.alter_column("datetime", server_default=text('now()'))
        batch_op.create_unique_constraint("uq_project_user", ["project_id", "user_id"])

    with op.batch_alter_table("a_project_location", "entity") as batch_op:
        batch_op.create_unique_constraint("uq_project_location", ["project_id", "location_id"])

    with op.batch_alter_table("a_project_tag", "entity") as batch_op:
        batch_op.create_unique_constraint("uq_project_tag", ["project_id", "tag_id"])

    with op.batch_alter_table("a_project_category", "entity") as batch_op:
        batch_op.create_unique_constraint("uq_project_category", ["project_id", "category_id"])

    with op.batch_alter_table("a_project_relation", "entity") as batch_op:
        batch_op.alter_column("score", new_column_name="similarity")
        batch_op.create_unique_constraint("uq_project_relation_project", ["project_id", "relation_project_id"])


def downgrade() -> None:
    with op.batch_alter_table("project", "entity") as batch_op:
        batch_op.alter_column("created", server_default=None)

    with op.batch_alter_table("a_project_member", "entity") as batch_op:
        batch_op.alter_column("joined", server_default=None)
        batch_op.drop_constraint("uq_project_member")

    with op.batch_alter_table("a_project_like", "entity") as batch_op:
        batch_op.alter_column("datetime", server_default=None)
        batch_op.drop_constraint("uq_project_user")

    with op.batch_alter_table("a_project_location", "entity") as batch_op:
        batch_op.create_unique_constraint("uq_project_location")

    with op.batch_alter_table("a_project_tag", "entity") as batch_op:
        batch_op.drop_constraint("uq_project_tag")

    with op.batch_alter_table("a_project_category", "entity") as batch_op:
        batch_op.drop_constraint("uq_project_category")

    with op.batch_alter_table("a_project_relation", "entity") as batch_op:
        batch_op.alter_column("similarity", new_column_name="score")
        batch_op.drop_constraint("uq_project_relation_project")
