from app.schemas.base import BaseModel
from app.schemas.user.user import UserShort


class OAuth2PasswordRequestForm(BaseModel):
    email: str
    password: str


class Tokens(BaseModel):
    access_token: str
    refresh_token: str


class TokenData(BaseModel):
    user_id: int
    exp: int


class Login(Tokens):
    user: UserShort
    is_admin: bool


class Signup(Login):
    pass
