from app.models.resource.type import type_table, a_type_extension_table
from app.models.resource.extension import extension_table
from app.repositories.base import BaseRepository
from sqlalchemy import select


class TypeRepository(BaseRepository):
    def __init__(self, connection):
        super(TypeRepository, self).__init__(connection, type_table)

    async def get_by_extension(self, extension: str):
        query = select(type_table).select_from(
            type_table.join(a_type_extension_table).join(extension_table)
        ).where(extension_table.c.mn == extension)
        record = await self.connection.execute(query)
        return record.fetchone()
