from app.schemas.base import BaseModel


class Category(BaseModel):
    id: int
    name: str


class PredictCategory(BaseModel):
    id: int
    name: str
    similarity: float
