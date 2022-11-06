from app.repositories.base import BaseRepository
from app.models.entity.stage import stage_table


class StageRepository(BaseRepository):
    def __init__(self, connection):
        super(StageRepository, self).__init__(connection, stage_table)
