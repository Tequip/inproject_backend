from app.repositories.entity.location import LocationRepository
from app.schemas.entity.location import Location


class LocationService:
    def __init__(self):
        pass

    @staticmethod
    async def get_by_project_id(db, project_id):
        location_repo = LocationRepository(db)
        location_records = await location_repo.get_by_project_id(project_id)
        return [Location(**location) for location in location_records]

    @staticmethod
    async def all(db):
        location_repo = LocationRepository(db)
        location_records = await location_repo.all()
        return [Location(**location) for location in location_records]

    @staticmethod
    async def get_by_event_id(db, event_id):
        location_repo = LocationRepository(db)
        location_records = await location_repo.get_by_event_id(event_id)
        return [Location(**location) for location in location_records]


location_service = LocationService()
