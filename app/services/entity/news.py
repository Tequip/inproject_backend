from app.repositories.entity.news import NewsRepository
from app.repositories.entity.project import ProjectRepository
from app.schemas.entity.news import News, NewsCreate
from app.api.error.base import HTTPExceptionPermission


class NewsService:
    def __init__(self):
        pass

    @staticmethod
    async def get_one(db, news_id):
        news_repo = NewsRepository(db)
        news_record = await news_repo.get_one(news_id)
        return News(**news_record)

    @staticmethod
    async def get_many(db, news_ids):
        news_repo = NewsRepository(db)
        news_records = await news_repo.get_many(news_ids)
        return [News(**news_record) for news_record in news_records]

    async def get_by_project(self, db, project_id):
        news_repo = NewsRepository(db)
        news_ids = await news_repo.get_by_project(project_id)
        return await self.get_many(db, news_ids)

    async def create(self, db, news_model: NewsCreate, user_id):
        project_repo = ProjectRepository(db)
        if await project_repo.is_member(news_model.project_id, user_id) or \
                await project_repo.is_owner(news_model.project_id, user_id):
            news_repo = NewsRepository(db)
            news_id = await news_repo.create(news_model)
            return self.get_one(db, news_id)
        else:
            raise HTTPExceptionPermission.project(news_model.project_id)


news_service = NewsService()
