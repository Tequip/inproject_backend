from typing import Optional

from app.schemas.base import BaseModel


class EventRelated(BaseModel):
    id: int
    name: str
    title_photo: Optional[str]

