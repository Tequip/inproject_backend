from app.schemas.base import BaseModel
from app.schemas.user.user import UserShort


class MemberBase(BaseModel):
    role: str


class Member(MemberBase):
    user: UserShort


class MemberCreate(MemberBase):
    user_id: int
