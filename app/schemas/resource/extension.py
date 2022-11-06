from app.schemas.base import BaseModel


class Extension(BaseModel):
    id: int
    name: str
    mn: str
    media_type: str
