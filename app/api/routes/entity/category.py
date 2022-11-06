from fastapi import APIRouter, Depends
from typing import List
from app.api.dependencies.db import get_db
from app.services.entity.category import category_service
from app.api.dependencies.user import get_current_user
from app.schemas.entity.category import Category

router = APIRouter()


@router.get("/category", response_model=List[Category])
async def skills(db=Depends(get_db), user_id=Depends(get_current_user)):
    return await category_service.all(db)
