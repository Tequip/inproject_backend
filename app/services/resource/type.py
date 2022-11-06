from app.repositories.resource.type import TypeRepository
from app.schemas.resource.type import Type


class TypeService:
    def __init__(self):
        pass

    async def get_by_extension(self, db, extension: str):
        type_repo = TypeRepository(db)
        type_ = await type_repo.get_by_extension(extension)
        if type_ is not None:
            return self.create_model_type(type_)

    @staticmethod
    def create_model_type(type_):
        return Type(id=type_["id"],
                    name=type_["name"])


type_service = TypeService()
