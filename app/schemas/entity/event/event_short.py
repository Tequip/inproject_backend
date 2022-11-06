from datetime import datetime

from app.schemas.entity.event.event_base import EventBase


class EventShort(EventBase):
    short_about: str
