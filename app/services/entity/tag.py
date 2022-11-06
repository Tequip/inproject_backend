from app.repositories.entity.tag import TagRepository
from app.schemas.entity.tag import Tag


class TagService:
    def __init__(self):
        pass

    @staticmethod
    async def get_by_project_id(db, project_id):
        tag_repo = TagRepository(db)
        tag_records = await tag_repo.get_by_project_id(project_id)
        return [Tag(**tag) for tag in tag_records]

    @staticmethod
    async def all(db):
        tag_repo = TagRepository(db)
        tag_records = await tag_repo.all()
        return [Tag(**tag) for tag in tag_records]

    @staticmethod
    async def get_by_event_id(db, project_id):
        tag_repo = TagRepository(db)
        tag_records = await tag_repo.get_by_event_id(project_id)
        return [Tag(**tag) for tag in tag_records]


tag_service = TagService()
