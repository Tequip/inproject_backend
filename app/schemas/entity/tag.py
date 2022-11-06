from app.schemas.base import BaseModel


class Tag(BaseModel):
    id: int
    name: str
