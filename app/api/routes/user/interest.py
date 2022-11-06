from fastapi import APIRouter, Depends
from typing import List
from app.api.dependencies.db import get_db
from app.services.interest import interest_service
from app.api.dependencies.user import get_current_user
from app.schemas.user.interest import Interest

router = APIRouter()


@router.get("/interest", response_model=List[Interest])
async def interest(db=Depends(get_db), user_id=Depends(get_current_user)):
    return await interest_service.all(db)
