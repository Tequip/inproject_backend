from sqlalchemy import Table, Column, Integer, Text, ForeignKey, DateTime, Float, Boolean, UniqueConstraint, text
from app.db.metadata import metadata

event_table = Table("event", metadata,
                    Column("id", Integer(), primary_key=True),
                    Column("title", Text(), nullable=False),
                    Column("owner_id", Integer(), ForeignKey("user.user.id")),
                    Column("is_hidden", Boolean(), nullable=False, server_default=text("False")),
                    Column("about", Text(), nullable=False),
                    Column("short_about", Text(), nullable=False),
                    Column("title_photo", Text(), nullable=True),
                    Column("source_url", Text(), nullable=True),
                    Column("created", DateTime(), nullable=False, server_default=text("now()")),
                    Column("start_date", DateTime(), nullable=False),
                    Column("end_date", DateTime(), nullable=False),
                    schema="entity")

a_event_location_table = Table("a_event_location", metadata,
                               Column("event_id", Integer(), ForeignKey("entity.event.id")),
                               Column("location_id", Integer(), ForeignKey("entity.location.id")),
                               UniqueConstraint("event_id", "location_id", name="uq_event_location"),
                               schema="entity")

a_event_tag_table = Table("a_event_tag", metadata,
                          Column("event_id", Integer(), ForeignKey("entity.event.id")),
                          Column("tag_id", Integer(), ForeignKey("entity.tag.id")),
                          UniqueConstraint("event_id", "tag_id", name="uq_event_tag"),
                          schema="entity")

a_event_category_table = Table("a_event_category", metadata,
                               Column("event_id", Integer(), ForeignKey("entity.event.id")),
                               Column("category_id", Integer(), ForeignKey("entity.category.id")),
                               UniqueConstraint("event_id", "category_id", name="uq_event_category"),
                               schema="entity")

a_event_relation_table = Table("a_event_relation", metadata,
                               Column("event_id", Integer(), ForeignKey("entity.event.id")),
                               Column("relation_event_id", Integer(), ForeignKey("entity.event.id")),
                               Column("similarity", Float(), nullable=False),
                               UniqueConstraint("event_id", "relation_event_id", name="uq_event_relation_event"),
                               schema="entity")
