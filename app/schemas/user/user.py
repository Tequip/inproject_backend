from typing import List, Optional
from app.schemas.base import BaseModel

from app.schemas.entity.project.project_short import ProjectShort
from app.schemas.resource.image import ImageCreate, Image
from app.schemas.user.skill import Skill
from app.schemas.user.interest import Interest


class UserBase(BaseModel):
    # TODO убрать имя фамилию
    first_name: Optional[str]
    last_name: Optional[str]
    email: str


class UserCreate(UserBase):
    password: str


class UserShort(UserBase):
    id: int
    telegram: Optional[str]
    about: Optional[str]
    status: Optional[str]
    role: Optional[str]
    photo: Optional[str]


class User(UserShort):
    skill: List[Skill]
    interest: List[Interest]
    project_creator: List[ProjectShort]
    project_member: List[ProjectShort]
    project_liked: List[ProjectShort]
    project_recommended: List[ProjectShort]
    is_admin: bool


class UserUpdate(UserBase):
    telegram: Optional[str]
    about: Optional[str]
    status: Optional[str]
    role: Optional[str]
    photo: Optional[ImageCreate]
    skill: List[int]
    interest: List[int]
