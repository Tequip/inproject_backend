from fastapi import APIRouter, Depends
from typing import List
from app.api.dependencies.db import get_db
from app.services.skill import skill_service
from app.api.dependencies.user import get_current_user
from app.schemas.user.skill import Skill

router = APIRouter()


@router.get("/skill", response_model=List[Skill])
async def skills(db=Depends(get_db), user_id=Depends(get_current_user)):
    return await skill_service.all(db)
