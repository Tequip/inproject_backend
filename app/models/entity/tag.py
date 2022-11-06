from sqlalchemy import Table, Column, Integer, String
from app.db.metadata import metadata

tag_table = Table("tag", metadata,
                  Column("id", Integer(), primary_key=True),
                  Column("name", String(200), nullable=False),
                  schema="entity")
