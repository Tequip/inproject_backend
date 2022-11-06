from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.api.dependencies.db import get_db
from app.services.user import user_service
from app.schemas.user.auth import Login

router = APIRouter()


@router.post("/auth", response_model=Login)
async def login(auth_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    return await user_service.login(db, auth_data.username, auth_data.password)
