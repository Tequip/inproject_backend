from typing import List, Optional
from sqlalchemy import select, delete, insert, exists, func, desc, and_, not_, or_
from app.repositories.base import BaseRepository
from app.models.entity.news import news_table
from app.models.entity.location import location_table
from app.models.entity.category import category_table
from app.schemas.entity.project.project import ProjectCreate


class NewsRepository(BaseRepository):
    def __init__(self, connection):
        super(NewsRepository, self).__init__(connection, news_table)

    async def get_by_project(self, project_id: int):
        query = select(news_table.c.id).where(news_table.c.project_id == project_id)
        records = await self.connection.execute(query)
        return [record["id"] for record in records]

    async def create(self, news_model):
        query = news_table.insert().values(title=news_model.title,
                                           text=news_model.text,
                                           project_id=news_model.project_id,
                                           ).returning(news_table.c.id)
        record = await self.connection.execute(query)
        return record.fetchone()["id"]


