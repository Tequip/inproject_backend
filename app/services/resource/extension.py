from app.repositories.resource.extension import ExtensionRepository
from app.schemas.resource.extension import Extension
from app.api.error.base import HTTPExceptionNotFound


class ExtensionService:
    def __init__(self):
        pass

    async def get_one(self, db, extension_id: int):
        extension_repo = ExtensionRepository(db)
        extension_record = await extension_repo.get_one(extension_id)
        if extension_record is None:
            raise HTTPExceptionNotFound.extension(extension_id)
        return self.create_model_extension(extension_record)

    async def get_by_extension(self, db, extension: str):
        extension_repo = ExtensionRepository(db)
        extension_record = await extension_repo.get_by_extension(extension)
        if extension_record is None:
            raise HTTPExceptionNotFound.extension_by_name(extension)
        return self.create_model_extension(extension_record)

    @staticmethod
    def create_model_extension(extension):
        return Extension(id=extension["id"],
                         name=extension["name"],
                         mn=extension["mn"],
                         media_type=extension["media_type"])


extension_service = ExtensionService()
