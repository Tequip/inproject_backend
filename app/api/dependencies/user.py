from app.services.security import security_service
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/swagger/auth/")


def get_current_user(token: str = Depends(oauth2_scheme)):
    return security_service.verify_token(token)

