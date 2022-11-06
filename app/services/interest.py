from app.repositories.user.interest import InterestRepository
from app.schemas.user.interest import Interest


class InterestService:
    def __init__(self):
        pass

    @staticmethod
    async def all(db):
        interest_repo = InterestRepository(db)
        interests = await interest_repo.all()
        return [Interest(**interest) for interest in interests]

    @staticmethod
    async def get_by_user(db, user_id: int):
        interest_repo = InterestRepository(db)
        interests = await interest_repo.get_by_user(user_id)
        return [Interest(**interest) for interest in interests]


interest_service = InterestService()
