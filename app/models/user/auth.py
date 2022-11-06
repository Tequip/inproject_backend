from sqlalchemy import Table, Column, Integer, String, ForeignKey

from app.db.metadata import metadata


auth_table = Table("auth", metadata,
                   Column("user_id", Integer(), ForeignKey("user.user.id"), primary_key=True),
                   Column("password_hash", String(400), nullable=False),
                   schema="user")

update_token_black_list_table = Table("update_token_white_list", metadata,
                                      Column("user_id", Integer(), ForeignKey("user.user.id")),
                                      Column("update_token", String(400), nullable=False),
                                      schema="user")
