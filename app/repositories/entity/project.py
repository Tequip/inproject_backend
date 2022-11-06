from typing import List, Optional
from sqlalchemy import select, delete, insert, exists, func, desc, and_, not_, or_
from app.repositories.base import BaseRepository
from app.models.entity.project import project_table, a_project_location_table, \
    a_project_category_table, a_project_relation_table, a_project_tag_table, \
    a_project_member_table, a_project_like_table, a_project_member_recommend_table
from app.models.entity.location import location_table
from app.models.entity.category import category_table
from app.schemas.entity.project.project import ProjectCreate


class ProjectRepository(BaseRepository):
    def __init__(self, connection):
        super(ProjectRepository, self).__init__(connection, project_table)

    async def get_many(self, project_ids: List[int], user_id: Optional[int] = None, limit: Optional[int] = 10):
        if user_id is None:
            query = select([project_table]).where(
                and_(project_table.c.id.in_(project_ids), not_(project_table.c.is_hidden))
            ).limit(limit)
        else:
            query = select([project_table.c.id.distinct(), project_table.c.title,
                            project_table.c.owner_id, project_table.c.about,
                            project_table.c.short_about, project_table.c.created,
                            project_table.c.deadline, project_table.c.likes,
                            project_table.c.stage_id, project_table.c.is_hidden]).select_from(
                project_table.join(a_project_member_table, isouter=True)
            ).where(
                and_(project_table.c.id.in_(project_ids),
                     or_(project_table.c.owner_id == user_id,
                         not_(project_table.c.is_hidden)
                         )
                     )
            ).limit(limit)
        records = await self.connection.execute(query)
        return records.fetchall()

    async def create(self, project_model: ProjectCreate):
        query = project_table.insert().values(title=project_model.title,
                                              about=project_model.about,
                                              short_about=project_model.short_about,
                                              owner_id=project_model.owner_id,
                                              deadline=project_model.deadline,
                                              stage_id=project_model.stage_id).returning(project_table.c.id)
        record = await self.connection.execute(query)
        return record.fetchone()["id"]

    async def insert_project_location(self, project_id: int, location_ids: List[int]) -> None:
        values = [{"project_id": project_id, "location_id": location_id} for location_id in set(location_ids)]
        await self.connection.execute(insert(a_project_location_table), values)

    async def delete_project_location(self, project_id: int, location_ids: List[int]) -> None:
        query = delete(a_project_location_table).where(
            and_(a_project_location_table.c.project_id == project_id,
                 a_project_location_table.c.location_id.in_(location_ids)))
        await self.connection.execute(query)

    async def insert_project_category(self, project_id: int, category_ids: List[int]) -> None:
        values = [{"project_id": project_id, "category_id": category_id} for category_id in set(category_ids)]
        await self.connection.execute(insert(a_project_category_table), values)

    async def delete_project_category(self, project_id: int, category_ids: List[int]) -> None:
        query = delete(a_project_category_table).where(
            and_(a_project_category_table.c.project_id == project_id,
                 a_project_category_table.c.category_id.in_(category_ids)))
        await self.connection.execute(query)

    async def insert_project_tag(self, project_id: int, tag_ids: List[int]) -> None:
        values = [{"project_id": project_id, "tag_id": tag_id} for tag_id in set(tag_ids)]
        await self.connection.execute(insert(a_project_tag_table), values)

    async def delete_project_tag(self, project_id: int, tag_ids: List[int]) -> None:
        query = delete(a_project_tag_table).where(
            and_(a_project_tag_table.c.project_id == project_id,
                 a_project_tag_table.c.tag_id.in_(tag_ids)))
        await self.connection.execute(query)

    async def get_short_recommended_by_user(self, user_id: int):
        query = select([a_project_member_recommend_table.c.project_id]).where(a_project_member_recommend_table.c.user_id == user_id)
        records = await self.connection.execute(query)
        return [record["project_id"] for record in records]

    async def get_by_query(self, query: str):
        query = select([project_table.c.id]).where(project_table.c.title.ilike("%{}%".format(query)))
        records = await self.connection.execute(query)
        return [record["id"] for record in records]

    async def get_by_location(self, location: List):
        query = select([project_table.c.id]).select_from(
            project_table.join(a_project_location_table).join(location_table)
        ).where(func.lower(location_table.c.name).in_(location))
        records = await self.connection.execute(query)
        return [record["id"] for record in records]

    async def get_by_category(self, category: List):
        query = select([project_table.c.id]).select_from(
            project_table.join(a_project_category_table).join(category_table)
        ).where(func.lower(category_table.c.name).in_(category))
        records = await self.connection.execute(query)
        return [record["id"] for record in records]

    async def get_by_like(self, limit: int):
        query = select([project_table.c.id]).where(
            not_(project_table.c.is_hidden)
        ).order_by(desc(project_table.c.likes)).limit(limit)
        records = await self.connection.execute(query)
        return [record["id"] for record in records]

    async def get_relation_project(self, project_id: int, limit: int = 5):
        query = select([a_project_relation_table.c.relation_project_id]).select_from(
            project_table.join(a_project_relation_table,
                               project_table.c.id == a_project_relation_table.c.relation_project_id)
        ).where(
            and_(a_project_relation_table.c.project_id == project_id,
                 not_(project_table.c.is_hidden)
                 )
        ).order_by(desc(a_project_relation_table.c.similarity)).limit(limit)

        records = await self.connection.execute(query)
        return [record["relation_project_id"] for record in records]

    async def get_by_owner(self, owner_id: int, limit: int):
        query = select([project_table.c.id]).where(
            project_table.c.owner_id == owner_id
        ).order_by(desc(project_table.c.created)).limit(limit)
        records = await self.connection.execute(query)
        return [record["id"] for record in records]

    async def get_by_member(self, member_id: int, limit: int):
        query = select([project_table.c.id]).select_from(
            project_table.join(a_project_member_table)
        ).where(
            a_project_member_table.c.member_id == member_id
        ).order_by(desc(project_table.c.created)).limit(limit)
        records = await self.connection.execute(query)
        return [record["id"] for record in records]

    async def get_by_user_like(self, user_id, limit: int):
        query = select([project_table.c.id]).select_from(
            project_table.join(a_project_like_table)
        ).where(
            a_project_like_table.c.user_id == user_id
        ).order_by(desc(a_project_like_table.c.datetime)).limit(limit)
        records = await self.connection.execute(query)
        return [record["id"] for record in records]

    async def is_owner(self, project_id: int, user_id: int) -> bool:
        query = select(exists(select(project_table.c.id).where(
            and_(project_table.c.id == project_id,
                 project_table.c.owner_id == user_id)
        )))
        record = await self.connection.execute(query)
        return record.scalar()

    async def is_member(self, project_id: int, user_id: int) -> bool:
        query = select(exists(select(project_table.c.id).select_from(project_table.join(a_project_member_table)).where(
            and_(project_table.c.id == project_id,
                 a_project_member_table.c.member_id == user_id)
        )))
        record = await self.connection.execute(query)
        return record.scalar()

    async def get_by_project_like(self, project_id, user_id):
        query = select([a_project_like_table.c.user_id]).select_from(
            project_table.join(a_project_member_table, isouter=True).join(a_project_like_table, isouter=True)
        ).where(
            and_(project_table.c.id == project_id,
                 or_(project_table.c.owner_id == user_id,
                     a_project_member_table.c.member_id == user_id,
                     not_(project_table.c.is_hidden)
                     )
                 )
        )
        records = await self.connection.execute(query)
        return [record["user_id"] for record in records.fetchall()]

    async def create_like(self, project_id: int, user_id: int):
        query = a_project_like_table.insert().values(project_id=project_id, user_id=user_id)
        await self.connection.execute(query)

    async def delete_like(self, project_id: int, user_id: int):
        query = delete(a_project_like_table).where(
            and_(a_project_like_table.c.project_id == project_id,
                 a_project_like_table.c.user_id == user_id))
        await self.connection.execute(query)
