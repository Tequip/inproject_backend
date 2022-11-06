from app.repositories.base import BaseRepository
from app.models.user.interest import interest_table
from app.models.user.user import a_user_interest_table

from sqlalchemy import select


class InterestRepository(BaseRepository):
    def __init__(self, connection):
        super(InterestRepository, self).__init__(connection, interest_table)

    async def get_by_user(self, user_id: int):
        query = select(interest_table).select_from(
            interest_table.join(a_user_interest_table)
        ).where(a_user_interest_table.c.user_id == user_id)
        records = await self.connection.execute(query)
        return records.fetchall()
