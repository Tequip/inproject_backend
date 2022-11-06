from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey, DateTime, Boolean, text

from app.db.metadata import metadata

user_table = Table("user", metadata,
                   Column("id", Integer(), primary_key=True),
                   Column("first_name", String(100), nullable=True),
                   Column("last_name", String(100), nullable=True),
                   Column("email", String(300), nullable=False),
                   Column("telegram", String(100), nullable=True),
                   Column("about", Text(), nullable=True),
                   Column("status", String(300), nullable=True),
                   Column("role", String(300), nullable=True),
                   Column("photo", String(200), nullable=True),
                   Column("birthday", DateTime(), nullable=True),
                   Column("is_hidden", Boolean(), nullable=False, server_default=text("False")),
                   Column("is_admin", Boolean(), nullable=True, server_default=text("False")),
                   schema="user")

a_user_interest_table = Table("a_user_interest", metadata,
                              Column("user_id", Integer(), ForeignKey("user.user.id")),
                              Column("interest_id", Integer(), ForeignKey("user.interest.id")),
                              schema="user")

a_user_skill_table = Table("a_user_skill", metadata,
                           Column("user_id", Integer(), ForeignKey("user.user.id")),
                           Column("skill_id", Integer(), ForeignKey("user.skill.id")),
                           schema="user")

