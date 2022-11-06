from fastapi import APIRouter, Depends
from typing import List
from app.api.dependencies.db import get_db
from app.services.entity.location import location_service
from app.api.dependencies.user import get_current_user
from app.schemas.entity.location import Location

router = APIRouter()


@router.get("/location", response_model=List[Location])
async def skills(db=Depends(get_db), user_id=Depends(get_current_user)):
    return await location_service.all(db)
