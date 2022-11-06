from sqlalchemy import Table, Column, Integer, Text, ForeignKey, DateTime, text
from app.db.metadata import metadata


news_table = Table("news", metadata,
                   Column("id", Integer(), primary_key=True),
                   Column("title", Text(), nullable=False),
                   Column("text", Text(), nullable=False),
                   Column("created", DateTime(), nullable=False, server_default=text("now()")),
                   Column("project_id", Integer(), ForeignKey("entity.project.id")),
                   schema="entity")
