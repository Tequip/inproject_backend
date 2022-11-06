from app.models.resource.extension import extension_table
from app.repositories.base import BaseRepository
from sqlalchemy import select


class ExtensionRepository(BaseRepository):
    def __init__(self, connection):
        super(ExtensionRepository, self).__init__(connection, extension_table)

    async def get_by_extension(self, extension: str):
        query = select(extension_table).where(extension_table.c.mn == extension)
        record = await self.connection.execute(query)
        return record.fetchone()
