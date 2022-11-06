from app.schemas.base import BaseModel
from typing import List, Optional
from app.schemas.entity.category import Category
from app.schemas.entity.location import Location
from app.schemas.entity.tag import Tag
from datetime import datetime


class ProjectBase(BaseModel):
    id: int
    title: str
    categories: Optional[List[Category]]
    locations: Optional[List[Location]]
    tags: Optional[List[Tag]]
    created: datetime
    likes: Optional[int]
