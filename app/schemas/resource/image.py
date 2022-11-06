from typing import Dict
from fastapi import File
from pydantic import root_validator


from app.schemas.base import BaseModel
from app.core.config import settings


class Image(BaseModel):
    id: int

    @property
    def url(self):
        return f'{settings.DOMAIN}{settings.RESOURCE_API}/{self.id}'

    @root_validator
    def generate_url(cls, values) -> Dict:
        values["url"] = f'{settings.DOMAIN}{settings.RESOURCE_API}/{values["id"]}'
        return values


class ImageCreate(BaseModel):
    file: str = File()
    filename: str
