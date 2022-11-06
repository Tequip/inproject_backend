from typing import List
from sqlalchemy import select, Table, exists


class BaseRepository:

    def __init__(self, connection, table: Table):
        self._connection = connection
        self._table = table

    @property
    def connection(self):
        return self._connection

    async def get_one(self, object_id: int):
        query = select([self._table]).where(self._table.c.id == object_id)
        record = await self.connection.execute(query)
        return record.fetchone()

    async def get_many(self, object_ids: List[int]):
        query = select([self._table]).where(self._table.c.id.in_(object_ids))
        records = await self.connection.execute(query)
        return records.fetchall()

    async def all(self):
        query = select(self._table.c.id)
        records = await self._connection.execute(query)
        return await self.get_many([record["id"] for record in records])

    async def exists(self, object_id: int):
        query = select(exists(select(self._table.c.id).where(self._table.c.id == object_id)))
        record = await self.connection.execute(query)
        return record.scalar()
