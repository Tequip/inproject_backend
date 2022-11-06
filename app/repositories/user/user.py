from app.repositories.base import BaseRepository
from app.models.user.user import user_table, a_user_skill_table, a_user_interest_table
from app.models.entity.project import a_project_member_recommend_table
from app.models.entity.project import a_project_member_table
from sqlalchemy import select, update, insert, delete, and_
from app.schemas.user.user import UserCreate, UserUpdate
from typing import List


class UserRepository(BaseRepository):
    def __init__(self, connection):
        super(UserRepository, self).__init__(connection, user_table)

    async def exists_by_email(self, email: str):
        query = select([user_table.c.id]).where(user_table.c.email == email)
        r = await self.connection.execute(query)
        return r.scalar()

    async def create(self, user_model: UserCreate):
        query = user_table.insert().values(first_name=user_model.first_name,
                                           last_name=user_model.last_name,
                                           email=user_model.email).returning(user_table.c.id)
        r = await self.connection.execute(query)
        return r.fetchone()

    async def update(self, user_id: int, user: UserUpdate):
        # TODO по идеи email надо проверять перед вставкой
        query = update(user_table).where(user_table.c.id == user_id).values(first_name=user["first_name"],
                                                                            last_name=user["last_name"],
                                                                            email=user["email"],
                                                                            telegram=user["telegram"],
                                                                            about=user["about"],
                                                                            status=user["status"],
                                                                            role=user["role"]).returning(user_table.c.id)
        r = await self.connection.execute(query)
        return r.fetchone()

    async def get_by_project(self, project_id: int):
        query = select([a_project_member_table.c.member_id]).where(a_project_member_table.c.project_id == project_id)
        records = await self.connection.execute(query)
        return [record["member_id"] for record in records]

    async def get_short_recommended_by_project(self, project_id: int):
        query = select([a_project_member_recommend_table.c.user_id]).where(
            a_project_member_recommend_table.c.project_id == project_id)
        records = await self.connection.execute(query)
        return [record["user_id"] for record in records]

    async def insert_user_skill(self, user_id: int, skill_ids: List[int]) -> None:
        values = [{"user_id": user_id, "skill_id": skill_id} for skill_id in set(skill_ids)]
        await self.connection.execute(insert(a_user_skill_table), values)

    async def delete_user_skill(self, user_id: int, skill_ids: List[int]) -> None:
        query = delete(a_user_skill_table).where(
            and_(a_user_skill_table.c.user_id == user_id,
                 a_user_skill_table.c.skill_id.in_(skill_ids)))
        await self.connection.execute(query)

    async def insert_user_interest(self, user_id: int, interest_ids: List[int]) -> None:
        values = [{"user_id": user_id, "interest_id": interest_id} for interest_id in set(interest_ids)]
        await self.connection.execute(insert(a_user_interest_table), values)

    async def delete_user_interest(self, user_id: int, interest_ids: List[int]) -> None:
        query = delete(a_user_interest_table).where(
            and_(a_user_interest_table.c.user_id == user_id,
                 a_user_interest_table.c.interest_id.in_(interest_ids)))
        await self.connection.execute(query)

