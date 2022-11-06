from sqlalchemy import Table, Column, Integer, String
from app.db.metadata import metadata

location_table = Table("location", metadata,
                       Column("id", Integer(), primary_key=True),
                       Column("name", String(200), nullable=False),
                       Column("iso", String(50), nullable=False),
                       schema="entity")
