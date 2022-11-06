from fastapi import APIRouter, Depends
from app.api.dependencies.db import get_db
from app.services.entity.stage import stage_service
from app.api.dependencies.user import get_current_user
from app.schemas.entity.stage import Stage
from typing import List

router = APIRouter()


@router.get("/stage", response_model=List[Stage])
async def skills(db=Depends(get_db), user_id=Depends(get_current_user)):
    return await stage_service.all(db)
