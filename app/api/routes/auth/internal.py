from fastapi import APIRouter, Depends
from app.schemas.user.auth import OAuth2PasswordRequestForm
from app.api.dependencies.db import get_db
from app.services.user import user_service
from app.schemas.user.user import UserCreate
from app.schemas.user.auth import Login, Signup

router = APIRouter()


@router.post("/auth", response_model=Login)
async def login(auth_data: OAuth2PasswordRequestForm, db=Depends(get_db)):
    return await user_service.login(db, auth_data.email, auth_data.password)


@router.post("/auth/signup", response_model=Signup)
async def signup(user: UserCreate, db=Depends(get_db)):
    return await user_service.create(db, user)

