from app.repositories.user.skill import SkillRepository
from app.schemas.user.skill import Skill


class SkillService:
    def __init__(self):
        pass

    @staticmethod
    async def all(db):
        skill_repo = SkillRepository(db)
        skills = await skill_repo.all()
        return [Skill(**skill) for skill in skills]

    @staticmethod
    async def get_by_user(db, user_id: int):
        skill_repo = SkillRepository(db)
        skills = await skill_repo.get_by_user(user_id)
        return [Skill(**skill) for skill in skills]


skill_service = SkillService()
