from typing import List, Optional

from app.schemas.base import BaseModel
from app.schemas.entity.category import Category
from app.schemas.entity.location import Location
from app.schemas.entity.tag import Tag
from app.schemas.resource.image import Image


class EventBase(BaseModel):
    id: int
    name: str
    title_photo: Optional[Image]
    locations: Optional[List[Location]]
    categories: Optional[List[Category]]
    tags: List[Tag]
