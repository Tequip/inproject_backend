from sqlalchemy import Table, Column, Integer, String
from app.db.metadata import metadata

extension_table = Table("extension", metadata,
                        Column("id", Integer(), primary_key=True),
                        Column("name", String(100), nullable=False),
                        Column("mn", String(10), nullable=False),
                        Column("media_type", String(100), nullable=False),
                        schema="resource")
