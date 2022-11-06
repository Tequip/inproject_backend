from sqlalchemy import Table, Column, Integer, String

from app.db.metadata import metadata


skill_table = Table("skill", metadata,
                    Column("id", Integer(), primary_key=True),
                    Column("name", String(200), nullable=False, unique=True),
                    schema="user")
