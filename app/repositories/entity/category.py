from app.models.entity.event import a_event_category_table
from app.repositories.base import BaseRepository
from app.models.entity.category import category_table
from app.models.entity.project import a_project_category_table, a_project_category_predict_table
from sqlalchemy import select, desc, insert, delete, and_


class CategoryRepository(BaseRepository):
    def __init__(self, connection):
        super(CategoryRepository, self).__init__(connection, category_table)

    async def get_by_project_id(self, project_id):
        query = select(category_table).select_from(
            category_table.join(a_project_category_table)
        ).where(a_project_category_table.c.project_id == project_id)
        records = await self.connection.execute(query)
        return records.fetchall()
    
    async def get_by_event_id(self, event_id):
        query = select(category_table).select_from(
            category_table.join(a_event_category_table)
        ).where(a_event_category_table.c.event_id == event_id)
        records = await self.connection.execute(query)
        return records.fetchall()

    async def get_predict_by_project(self, project_id):
        query = select([category_table.c.id,
                        category_table.c.name,
                        a_project_category_predict_table.c.similarity]
                       ).select_from(category_table.join(a_project_category_predict_table)
                                     ).where(a_project_category_predict_table.c.project_id == project_id).order_by(
            desc(a_project_category_predict_table.c.similarity))
        records = await self.connection.execute(query)
        return records.fetchall()

    async def insert_event_categories(self, event_id, categories_ids):
        values = [{"event_id": event_id, "category_id": category_id} for category_id in set(categories_ids)]
        await self.connection.execute(insert(a_event_category_table), values)

    async def delete_event_categories(self, event_id, categories_ids):
        query = delete(a_event_category_table).where(
            and_(a_event_category_table.c.event_id == event_id,
                 a_event_category_table.c.category_id.in_(categories_ids)))
        await self.connection.execute(query)
