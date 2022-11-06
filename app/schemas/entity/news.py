from app.schemas.base import BaseModel
from datetime import datetime


class NewsBase(BaseModel):
    title: str
    text: str
    created: datetime


class News(NewsBase):
    id: int


class NewsCreate(NewsBase):
    project_id: int
