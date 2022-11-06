from app.models.entity.event import a_event_tag_table
from app.repositories.base import BaseRepository
from app.models.entity.tag import tag_table
from app.models.entity.project import a_project_tag_table
from sqlalchemy import select, insert, delete, and_


class TagRepository(BaseRepository):
    def __init__(self, connection):
        super(TagRepository, self).__init__(connection, tag_table)

    async def get_by_project_id(self, project_id):
        query = select(tag_table).select_from(
            tag_table.join(a_project_tag_table)
        ).where(a_project_tag_table.c.project_id == project_id)
        records = await self.connection.execute(query)
        return records.fetchall()
    
    async def get_by_event_id(self, event_id):
        query = select(tag_table).select_from(
            tag_table.join(a_event_tag_table)
        ).where(a_event_tag_table.c.event_id == event_id)
        records = await self.connection.execute(query)
        return records.fetchall()

    async def insert_event_tags(self, event_id, tags_ids):
        values = [{"event_id": event_id, "tag_id": tag_id} for tag_id in set(tags_ids)]
        await self.connection.execute(insert(a_event_tag_table), values)

    async def delete_event_tags(self, event_id, tags_ids):
        query = delete(a_event_tag_table).where(
            and_(a_event_tag_table.c.event_id == event_id,
                 a_event_tag_table.c.location_id.in_(tags_ids)))
        await self.connection.execute(query)
