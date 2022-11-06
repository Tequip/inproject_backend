from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Float, UniqueConstraint, text
from app.db.metadata import metadata

project_table = Table("project", metadata,
                      Column("id", Integer(), primary_key=True),
                      Column("title", Text(), nullable=False),
                      Column("owner_id", Integer(), ForeignKey("user.user.id"), nullable=False),
                      Column("about", Text(), nullable=False),
                      Column("short_about", Text(), nullable=False),
                      Column("created", DateTime(), nullable=False, server_default=text("now()")),
                      Column("deadline", DateTime(), nullable=True),
                      Column("likes", Integer(), nullable=True, server_default=text("0")),
                      Column("stage_id", Integer(), ForeignKey("entity.stage.id"), nullable=True),
                      Column("is_hidden", Boolean(), nullable=True, server_default=text("False")),
                      schema="entity")


a_project_member_table = Table("a_project_member", metadata,
                               Column("project_id", Integer(), ForeignKey("entity.project.id")),
                               Column("member_id", Integer(), ForeignKey("user.user.id")),
                               Column("active", Boolean(), nullable=False),
                               Column("joined", DateTime(), nullable=False, server_default=text("now()")),
                               Column("removed", DateTime(), nullable=True),
                               Column("role", String(200), nullable=False),
                               UniqueConstraint("project_id", "member_id", name="uq_project_member"),
                               schema="entity")

a_project_like_table = Table("a_project_like", metadata,
                             Column("project_id", Integer(), ForeignKey("entity.project.id")),
                             Column("user_id", Integer(), ForeignKey("user.user.id")),
                             Column("datetime", DateTime(), nullable=False, server_default=text('now()')),
                             UniqueConstraint("project_id", "user_id", name="uq_project_user"),
                             schema="entity")

a_project_location_table = Table("a_project_location", metadata,
                                 Column("project_id", Integer(), ForeignKey("entity.project.id")),
                                 Column("location_id", Integer(), ForeignKey("entity.location.id")),
                                 UniqueConstraint("project_id", "location_id", name="uq_project_location"),
                                 schema="entity")

a_project_tag_table = Table("a_project_tag", metadata,
                            Column("project_id", Integer(), ForeignKey("entity.project.id")),
                            Column("tag_id", Integer(), ForeignKey("entity.tag.id")),
                            UniqueConstraint("project_id", "tag_id", name="uq_project_tag"),
                            schema="entity")

a_project_category_table = Table("a_project_category", metadata,
                                 Column("project_id", Integer(), ForeignKey("entity.project.id")),
                                 Column("category_id", Integer(), ForeignKey("entity.category.id")),
                                 UniqueConstraint("project_id", "category_id", name="uq_project_category"),
                                 schema="entity")

a_project_relation_table = Table("a_project_relation", metadata,
                                 Column("project_id", Integer(), ForeignKey("entity.project.id")),
                                 Column("relation_project_id", Integer(), ForeignKey("entity.project.id")),
                                 Column("similarity", Float(), nullable=False),
                                 UniqueConstraint("project_id", "relation_project_id",
                                                  name="uq_project_relation_project"),
                                 schema="entity")

a_project_member_order_table = Table("a_project_member_order", metadata,
                                     Column("project_id", Integer(), ForeignKey("entity.project.id")),
                                     Column("role", String(200), nullable=False),
                                     schema="entity"
                                     )

a_project_member_recommend_table = Table("a_project_member_recommend", metadata,
                                         Column("project_id", Integer(), ForeignKey("entity.project.id")),
                                         Column("user_id", Integer(), ForeignKey("user.user.id")),
                                         Column("fits", Float(), nullable=False),
                                         schema="entity")

a_project_category_predict_table = Table("a_project_category_predict", metadata,
                                         Column("project_id", Integer(), ForeignKey("entity.project.id")),
                                         Column("category_id", Integer(), ForeignKey("entity.category.id")),
                                         Column("similarity", Float(), nullable=False),
                                         schema="entity")
