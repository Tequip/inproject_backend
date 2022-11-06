from app.repositories.entity.stage import StageRepository
from app.schemas.entity.stage import Stage
from app.api.error.base import HTTPExceptionNotFound


class StageService:
    def __init__(self):
        pass

    @staticmethod
    async def get_one(db, stage_id):
        stage_repo = StageRepository(db)
        stage_record = await stage_repo.get_one(stage_id)
        if stage_record is None:
            raise HTTPExceptionNotFound.stage(stage_id)
        return Stage(**stage_record)

    @staticmethod
    async def all(db):
        stage_repo = StageRepository(db)
        stage_records = await stage_repo.all()
        return [Stage(**stage) for stage in stage_records]


stage_service = StageService()
