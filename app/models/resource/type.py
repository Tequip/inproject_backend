from sqlalchemy import Table, Column, Integer, String, ForeignKey
from app.db.metadata import metadata

type_table = Table("type", metadata,
                   Column("id", Integer(), primary_key=True),
                   Column("name", String(100), nullable=False),
                   schema="resource")

a_type_extension_table = Table("a_type_extension", metadata,
                               Column("type_id", Integer(), ForeignKey("resource.type.id")),
                               Column("extension_id", Integer(), ForeignKey("resource.extension.id")),
                               schema="resource")
