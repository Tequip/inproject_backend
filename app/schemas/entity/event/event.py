from datetime import datetime
from typing import List, Optional

from app.schemas.entity.event.event_base import EventBase
from app.schemas.entity.event.event_related import EventRelated
from app.schemas.user.user import UserShort


class Event(EventBase):
    owner: Optional[UserShort]
    about: str
    start_date: datetime
    end_date: datetime
    created_date: Optional[datetime]
    is_hidden: bool
    source_url: Optional[str]
    related_events: Optional[List[EventRelated]]
