from typing import Dict
from passlib.context import CryptContext
from jose import jwt, JWTError
from app.core.config import settings
from datetime import datetime, timedelta
from app.api.error.base import HTTPExceptionAuth
from app.schemas.user.auth import Tokens, TokenData


class SecurityService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_key_pair(self, payload: Dict):
        return Tokens(access_token=self.create_access_token(payload),
                      refresh_token=self.create_refresh_token(payload))

    def create_access_token(self, payload: Dict):
        expire_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return self.create_token(payload, expire_delta)

    def create_refresh_token(self, payload: Dict):
        expire_delta = timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return self.create_token(payload, expire_delta)

    @staticmethod
    def create_token(payload: Dict, expire_delta: timedelta) -> str:
        expire = datetime.utcnow() + expire_delta
        return jwt.encode({**payload, "exp": expire}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    def verify_token(token: str):
        try:
            token_data = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        except JWTError:
            raise HTTPExceptionAuth.bad_token()

        if token_data["exp"] < datetime.utcnow().timestamp():
            raise HTTPExceptionAuth.expire_token()

        return TokenData(user_id=token_data["user_id"], exp=token_data["exp"])

    def hashing_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)


security_service = SecurityService()
