from pydantic import BaseModel as PydanticBaseModel
from collections.abc import Mapping


class BaseModel(PydanticBaseModel, Mapping):

    def __getitem__(self, key):
        return getattr(self, key)

    def __iter__(self):
        yield from self.__dict__.__iter__()

    def __len__(self):
        return self.__dict__.__len__()
