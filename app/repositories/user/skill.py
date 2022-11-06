from app.repositories.base import BaseRepository
from app.models.user.skill import skill_table
from app.models.user.user import a_user_skill_table

from sqlalchemy import select


class SkillRepository(BaseRepository):
    def __init__(self, connection):
        super(SkillRepository, self).__init__(connection, skill_table)

    async def get_by_user(self, user_id: int):
        query = select(skill_table).select_from(
            skill_table.join(a_user_skill_table)
        ).where(a_user_skill_table.c.user_id == user_id)
        records = await self.connection.execute(query)
        return records.fetchall()
