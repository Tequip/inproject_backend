from typing import List

from app.repositories.entity.member import MemberRepository
from app.schemas.entity.project.member import Member, MemberCreate
from app.services.user import user_service


class MemberService:
    def __init__(self):
        pass

    async def get_by_project_id(self, db, project_id):
        member_repo = MemberRepository(db)
        member_records = await member_repo.get_by_project_id(project_id)
        return await self.create_model_members(db, member_records)

    @staticmethod
    async def update_remove_status(db, project_id: int, member_ids: List[int]):
        member_repo = MemberRepository(db)
        await member_repo.update_remove_status(project_id, member_ids)

    @staticmethod
    async def upsert(db, project_id: int, members_model: List[MemberCreate]):
        member_repo = MemberRepository(db)
        await member_repo.upsert(project_id, members_model)

    async def create_model_members(self, db, member_records):
        return [await self.create_model_member(db, record) for record in member_records]

    @staticmethod
    async def create_model_member(db, member_record):
        user = await user_service.get_short_one(db, member_record["member_id"])
        return Member(
            user=user,
            role=member_record["role"])


member_service = MemberService()
