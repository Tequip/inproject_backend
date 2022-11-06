from datetime import datetime
from typing import Optional, List

from app.schemas.base import BaseModel
from app.schemas.entity.category import Category
from app.schemas.entity.event.event_related import EventRelated
from app.schemas.entity.location import Location
from app.schemas.entity.tag import Tag
from app.schemas.resource.image import ImageCreate
from app.schemas.user.user import UserShort


class EventCreate(BaseModel):
    id: int
    name: str
    title_photo: Optional[ImageCreate]
    locations: Optional[List[Location]]
    categories: Optional[List[Category]]
    tags: List[Tag]
    owner: Optional[UserShort]
    about: str
    start_date: datetime
    end_date: datetime
    created_date: Optional[datetime]
    is_hidden: bool
    source_url: Optional[str]
    related_events: Optional[List[EventRelated]]

