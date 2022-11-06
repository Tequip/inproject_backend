from typing import List

from app.models.entity.event import a_event_location_table
from app.repositories.base import BaseRepository
from app.models.entity.location import location_table
from app.models.entity.project import a_project_location_table
from sqlalchemy import select, insert, delete, and_


class LocationRepository(BaseRepository):
    def __init__(self, connection):
        super(LocationRepository, self).__init__(connection, location_table)

    async def get_by_project_id(self, project_id):
        query = select(location_table).select_from(
            location_table.join(a_project_location_table)
        ).where(a_project_location_table.c.project_id == project_id)
        records = await self.connection.execute(query)
        return records.fetchall()
    
    async def get_by_event_id(self, event_id):
        query = select(location_table).select_from(
            location_table.join(a_event_location_table)
        ).where(a_event_location_table.c.event_id == event_id)
        records = await self.connection.execute(query)
        return records.fetchall()

    async def insert_event_locations(self, event_id, location_ids: List[int]):
        values = [{"event_id": event_id, "location_id": location_id} for location_id in set(location_ids)]
        await self.connection.execute(insert(a_event_location_table), values)

    async def delete_event_locations(self, event_id, location_ids: List[int]):
        query = delete(a_event_location_table).where(
            and_(a_event_location_table.c.event_id == event_id,
                 a_event_location_table.c.location_id.in_(location_ids)))
        await self.connection.execute(query)

