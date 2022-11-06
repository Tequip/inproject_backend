from sqlalchemy import select, insert, delete, and_
from app.models.entity.category import category_table
from app.models.entity.event import a_event_category_table


class CategoryRepository:
    def __init__(self, connection):
        self._connection = connection

    @property
    def connection(self):
        return self._connection

    def get_many(self, category_ids):
        query = select([category_table]).where(category_table.c.id.in_(category_ids))
        records = self.connection.execute(query)
        return records.fetchall()

    def all(self):
        query = select(category_table.c.id)
        records = self._connection.execute(query)
        return self.get_many([record["id"] for record in records])

