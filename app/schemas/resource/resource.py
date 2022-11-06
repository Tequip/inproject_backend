from typing import Optional, Dict
from fastapi import File
from pydantic import root_validator

from app.schemas.resource.type import Type
from app.schemas.resource.extension import Extension
from app.schemas.base import BaseModel
from app.core.config import settings


class Resource(BaseModel):
    id: int

    @property
    def url(self):
        return f'{settings.DOMAIN}{settings.RESOURCE_API}/{self.id}'

    @root_validator
    def generate_url(cls, values) -> Dict:
        values["url"] = f'{settings.DOMAIN}{settings.RESOURCE_API}/{values["id"]}'
        return values


class ResourceInfo(BaseModel):
    id: int
    type: Optional[Type]
    original_name: str
    extension: Extension


class ResourceCreate(BaseModel):
    file: str = File()
    filename: str

