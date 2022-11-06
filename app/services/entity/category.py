from app.repositories.entity.category import CategoryRepository
from app.schemas.entity.category import Category,PredictCategory


class CategoryService:
    def __init__(self):
        pass

    @staticmethod
    async def get_by_project_id(db, project_id):
        category_repo = CategoryRepository(db)
        category_records = await category_repo.get_by_project_id(project_id)
        return [Category(**category) for category in category_records]

    @staticmethod
    async def all(db):
        category_repo = CategoryRepository(db)
        category_records = await category_repo.all()
        return [Category(**category) for category in category_records]

    @staticmethod
    async def get_by_event_id(db, event_id):
        category_repo = CategoryRepository(db)
        category_records = await category_repo.get_by_event_id(event_id)
        return [Category(**category) for category in category_records]

    @staticmethod
    async def get_predict_by_project(db, project_id):
        category_repo = CategoryRepository(db)
        category_records = await category_repo.get_predict_by_project(project_id)
        return [PredictCategory(**category) for category in category_records]


category_service = CategoryService()
