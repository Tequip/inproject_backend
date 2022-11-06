from fastapi import APIRouter, Depends
from typing import List
from app.api.dependencies.db import get_db
from app.services.entity.tag import tag_service
from app.api.dependencies.user import get_current_user
from app.schemas.entity.tag import Tag

router = APIRouter()


@router.get("/tag", response_model=List[Tag])
async def skills(db=Depends(get_db), user_id=Depends(get_current_user)):
    return await tag_service.all(db)
