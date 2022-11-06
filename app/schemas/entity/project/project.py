from app.schemas.base import BaseModel
from app.schemas.entity.project.project_base import ProjectBase
from typing import List, Optional
from app.schemas.user.user import UserShort
from app.schemas.entity.project.project_short import ProjectShort
from datetime import datetime
from app.schemas.entity.project.member import MemberCreate, Member
from app.schemas.resource.image import Image, ImageCreate
from app.schemas.entity.news import News


class Project(ProjectBase):
    images: List[Image]
    about: str
    owner: UserShort
    deadline: Optional[datetime]
    members: List[Member]
    is_project_owner: bool
    is_project_member: bool
    is_hidden: bool
    related_projects: List[ProjectShort]
    user_recommended: List[UserShort]
    stage: Optional[str]
    news: List[News]


class ProjectCreate(BaseModel):
    title: str
    images: List[ImageCreate]
    about: str
    short_about: str
    owner_id: int
    members: List[MemberCreate]
    categories: List[int]
    locations: List[int]
    tags: List[int]
    deadline: Optional[datetime]
    is_hidden: Optional[bool]
    stage_id: Optional[int]
