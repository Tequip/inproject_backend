from typing import Optional, List
from app.schemas.entity.project.project_base import ProjectBase
from app.schemas.base import BaseModel


class ProjectShort(ProjectBase):
    image: Optional[str]
    about: str


class Page(BaseModel):
    max_page: int
    current_page: Optional[int]
    projects: List[ProjectShort]
