from sqlalchemy import delete, select, distinct, not_
from app.models.user.user import user_table, a_user_interest_table
from app.models.user.interest import interest_table


class UserRepository:
    def __init__(self, connection):
        self._connection = connection

    @property
    def connection(self):
        return self._connection

    def get_many(self, user_ids):
        query = select([user_table]).where(user_table.c.id.in_(user_ids))
        records = self.connection.execute(query)
        return records.fetchall()

    def all(self):
        query = select(distinct(user_table.c.id)).select_from(
            user_table.join(a_user_interest_table)).where(not_(user_table.c.is_hidden))
        records = self._connection.execute(query)
        return self.get_many([record["id"] for record in records])

    def get_interest(self, user_id):
        query = select(interest_table.c.name).select_from(
            interest_table.join(a_user_interest_table)
        ).where(a_user_interest_table.c.user_id == user_id)
        records = self.connection.execute(query)
        return [record["name"] for record in records]
