from typing import List, Optional

from sqlalchemy import select, func, not_, and_, desc, update, insert

from app.models.entity.category import category_table
from app.models.entity.event import event_table, a_event_location_table, a_event_category_table, a_event_relation_table
from app.models.entity.location import location_table
from app.repositories.base import BaseRepository
from app.schemas.entity.event.event import Event


class EventRepository(BaseRepository):
    def __init__(self, connection):
        super(EventRepository, self).__init__(connection, event_table)

    async def get_many(self, event_ids: List[int], limit: Optional[int] = 10):
        query = select([event_table]).where(
            and_(event_table.c.id.in_(event_ids), not_(event_table.c.is_hidden))
        ).limit(limit)
        records = await self.connection.execute(query)
        return records.fetchall()

    async def all(self, limit: Optional[int] = 10):
        query = select([event_table]).limit(limit)
        records = await self.connection.execute(query)
        return records.fetchall()

    async def get_by_query(self, query: str):
        query = select([event_table.c.id]).where(event_table.c.about.ilike("%{}%".format(query)))
        records = await self.connection.execute(query)
        return [record["id"] for record in records]

    async def get_by_location(self, location: List):
        query = select([event_table.c.id]).select_from(
            event_table.join(a_event_location_table).join(location_table)
        ).where(func.lower(location_table.c.name).in_(location))
        records = await self.connection.execute(query)
        return [record["id"] for record in records]

    async def get_by_category(self, category: List):
        query = select([event_table.c.id]).select_from(
            event_table.join(a_event_category_table).join(category_table)
        ).where(func.lower(category_table.c.name).in_(category))
        records = await self.connection.execute(query)
        return [record["id"] for record in records]

    async def get_related_events(self, event_id, limit: int = 5):
        query = select([a_event_relation_table.c.relation_event_id]).select_from(
            event_table.join(a_event_relation_table,
                             event_table.c.id == a_event_relation_table.c.relation_event_id)
        ).where(
            and_(a_event_relation_table.c.event_id == event_id,
                 not_(event_table.c.is_hidden)
                 )
        ).order_by(desc(a_event_relation_table.c.similarity)).limit(limit)

        records = await self.connection.execute(query)
        return [record["relation_event_id"] for record in records]

    async def update(self, event: Event):
        query = update(event_table).where(event_table.c.id == event.id).values(
            title=event.name,
            about=event.about,
            start_date=event.start_date,
            end_date=event.end_date,
            source_url=event.source_url,
            is_hidden=event.is_hidden).returning(event_table.c.id)
        r = await self.connection.execute(query)
        return r.fetchone()

    async def create(self, event: Event):
        query = insert(event_table).values(
            name=event.name,
            about=event.about,
            start_date=event.start_date,
            end_date=event.end_date,
            source_url=event.source_url,
            is_hidden=event.is_hidden).returning(event_table.c.id)
        r = await self.connection.execute(query)
        return r.fetchone()
