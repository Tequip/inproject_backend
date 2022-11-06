from sqlalchemy import Table, Column, Integer, String, ForeignKey

from app.db.metadata import metadata

resource_table = Table("resource", metadata,
                       Column("id", Integer(), primary_key=True),
                       Column("path", String(100), nullable=False),
                       Column("original_name", String(255), nullable=False),
                       Column("extension_id", Integer(), ForeignKey("resource.extension.id")),
                       schema="resource")

a_resource_project_table = Table("a_resource_project", metadata,
                                 Column("resource_id", Integer(), ForeignKey("resource.resource.id")),
                                 Column("project_id", Integer(), ForeignKey("entity.project.id")),
                                 schema="resource")

a_resource_event_table = Table("a_resource_event", metadata,
                               Column("resource_id", Integer(), ForeignKey("resource.resource.id")),
                               Column("event_id", Integer(), ForeignKey("entity.event.id")),
                               schema="resource")

a_image_project_table = Table("a_image_project", metadata,
                              Column("resource_id", Integer(), ForeignKey("resource.resource.id")),
                              Column("project_id", Integer(), ForeignKey("entity.project.id")),
                              schema="resource")

a_image_event_table = Table("a_image_event", metadata,
                            Column("resource_id", Integer(), ForeignKey("resource.resource.id")),
                            Column("event_id", Integer(), ForeignKey("entity.event.id")),
                            schema="resource")

a_image_user_table = Table("a_image_user", metadata,
                           Column("resource_id", Integer(), ForeignKey("resource.resource.id")),
                           Column("user_id", Integer(), ForeignKey("user.user.id")),
                           schema="resource")
