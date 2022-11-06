from typing import List, Optional

from fastapi import APIRouter, Depends
from starlette import status

from app.api.dependencies.db import get_db
from app.api.dependencies.user import get_current_user
from app.schemas.entity.event.event import Event
from app.schemas.entity.event.event_create import EventCreate
from app.schemas.entity.event.event_short import EventShort
from app.services.entity.event import event_service

router = APIRouter()

standard_responses = {
    status.HTTP_404_NOT_FOUND: {"description": "Item not found"},
    status.HTTP_200_OK: {"description": "Ok"}
}


@router.get("/events", response_model=List[EventShort])
async def get_all_events(query: Optional[str] = None,
                         location: Optional[str] = None,
                         category: Optional[str] = None,
                         # page: Optional[int] = None,
                         limit: Optional[int] = None,
                         db=Depends(get_db),
                         _=Depends(get_current_user)):
    return await event_service.get_many_by_query_location_category(db, query, location, category, limit)


@router.get("/event/{id}", response_model=Event, responses={**standard_responses})
async def get_event(id: int, db=Depends(get_db), _=Depends(get_current_user)):
    return await event_service.get_one_by_id(db, id)


@router.put("/event/", status_code=status.HTTP_201_CREATED)
async def update_event(event: EventCreate, db=Depends(get_db), user=Depends(get_current_user)):
    return await event_service.update_event(db, event, user)


@router.post("/event", status_code=status.HTTP_201_CREATED)
async def create_event(event: EventCreate, db=Depends(get_db), user=Depends(get_current_user)):
    return await event_service.create_event(db, event, user)
