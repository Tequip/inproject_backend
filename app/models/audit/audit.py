from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime, String, Text
from app.db.metadata import metadata

audit_table = Table("audit", metadata,
                    Column("ts", DateTime(), primary_key=True, nullable=False),
                    Column("user_id", Integer(), ForeignKey("user.user.id"), primary_key=True, nullable=False),
                    Column("method", String(100), nullable=False),
                    Column("url", Text(), nullable=False),
                    Column("agent", Text()),
                    Column("params", Text()),
                    schema="audit")
