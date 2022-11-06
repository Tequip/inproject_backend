from app.repositories.base import BaseRepository
from app.models.user.auth import auth_table
from sqlalchemy import select


class AuthRepository(BaseRepository):
    def __init__(self, connection):
        super(AuthRepository, self).__init__(connection, auth_table)

    async def get_hashed_password(self, user_id: int):
        query = select([auth_table.c.password_hash]).where(auth_table.c.user_id == user_id)
        record = await self.connection.execute(query)
        return record.fetchone()

    async def create(self, user_id, hashed_password: str):
        query = auth_table.insert().values(user_id=user_id, password_hash=hashed_password)
        await self.connection.execute(query)
