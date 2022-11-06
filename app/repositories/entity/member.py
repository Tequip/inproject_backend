from app.models.entity.project import a_project_member_table
from app.schemas.entity.project.member import MemberCreate
from sqlalchemy import select, update, and_
from sqlalchemy.dialects import postgresql
from typing import List
from datetime import datetime


class MemberRepository:
    def __init__(self, connection):
        self._connection = connection

    @property
    def connection(self):
        return self._connection

    async def get_by_project_id(self, project_id: int):
        query = select(a_project_member_table).where(a_project_member_table.c.project_id == project_id)
        records = await self.connection.execute(query)
        return records.fetchall()

    async def update_remove_status(self, project_id: int, member_ids: List[int]):
        query = update(a_project_member_table).where(
            and_(a_project_member_table.c.project_id == project_id,
                 a_project_member_table.c.member_id.in_(member_ids))
        ).values(active=False, removed=datetime.utcnow())
        await self.connection.execute(query)

    async def upsert(self, project_id: int, members: List[MemberCreate]):
        values = [{"project_id": project_id,
                   "member_id": member.user_id,
                   "role": member.role,
                   "active": True,
                   "removed": None} for member in members]
        insert = postgresql.insert(a_project_member_table)
        await self.connection.execute(insert.on_conflict_do_update(
            index_elements=[a_project_member_table.c.project_id, a_project_member_table.c.member_id],
            set_={"role": insert.excluded.role,
                  "active": insert.excluded.active,
                  "removed": insert.excluded.removed}), values)

