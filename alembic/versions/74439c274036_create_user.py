"""Create user

Revision ID: 74439c274036
Revises: 
Create Date: 2022-10-06 21:40:47.400916

"""
from alembic import op
from sqlalchemy import Column, Integer, String, ForeignKey


# revision identifiers, used by Alembic.
revision = '74439c274036'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('CREATE SCHEMA "user"')
    op.create_table(
        "user",
        Column("id", Integer(), primary_key=True),
        Column("first_name", String(50), nullable=False),
        Column("last_name", String(50), nullable=False),
        Column("email", String(200), nullable=False),
        Column("telegram", String(50), nullable=True),
        Column("about", String(), nullable=True),
        Column("status", String(50), nullable=True),
        Column("role", String(50), nullable=False),
        Column("photo", String(200), nullable=True),
        schema="user"
    )

    interest_table = op.create_table(
        "interest",
        Column("id", Integer(), primary_key=True),
        Column("name", String(50), nullable=False, unique=True),
        schema="user"
    )

    skill_table = op.create_table(
        "skill",
        Column("id", Integer(), primary_key=True),
        Column("name", String(50), nullable=False, unique=True),
        schema="user"
    )

    op.create_table(
        "a_user_interest",
        Column("user_id", Integer(), ForeignKey("user.user.id")),
        Column("interest_id", Integer(), ForeignKey("user.interest.id")),
        schema="user"
    )

    op.create_table(
        "a_user_skill",
        Column("user_id", Integer(), ForeignKey("user.user.id")),
        Column("skill_id", Integer(), ForeignKey("user.skill.id")),
        schema="user"
    )

    op.bulk_insert(interest_table, [{"id": 1, "name": "Чтение"},
                                    {"id": 2, "name": "Прогулки"},
                                    {"id": 3, "name": "Программирование"},
                                    ])

    op.bulk_insert(skill_table, [{"id": 1, "name": "Управление людьми"},
                                 {"id": 2, "name": "Креативность"},
                                 {"id": 3, "name": "Быстрое обучение"}
                                 ])


def downgrade() -> None:
    op.drop_table('a_user_skill', schema="user")
    op.drop_table('a_user_interest', schema="user")
    op.drop_table('skill', schema="user")
    op.drop_table('interest', schema="user")
    op.drop_table('user', schema="user")
    op.execute('DROP SCHEMA "user"')
