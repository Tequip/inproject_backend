from typing import List, Optional
from fastapi import APIRouter, Depends
from app.api.dependencies.db import get_db
from app.services.user import user_service
from app.api.dependencies.user import get_current_user
from app.schemas.user.user import User, UserShort, UserUpdate

router = APIRouter()


@router.get("/user", response_model=User)
async def get_user(db=Depends(get_db), token=Depends(get_current_user)):
    return await user_service.get_one(db, token.user_id, token.user_id)


@router.put("/user", response_model=User)
async def update_user(user: UserUpdate, db=Depends(get_db), token=Depends(get_current_user)):
    return await user_service.update(db, token.user_id, user)


@router.get("/user/{user_id}", response_model=User)
async def get_user_by_id(user_id: int, db=Depends(get_db), token=Depends(get_current_user)):
    return await user_service.get_one(db, user_id, token.user_id)


@router.get("/users", response_model=List[UserShort])
async def get_users(q: Optional[str] = None, db=Depends(get_db), token=Depends(get_current_user)):
    return await user_service.all(db)

