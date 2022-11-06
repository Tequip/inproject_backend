from typing import List, Optional

from fastapi import APIRouter, Depends, UploadFile, File, status

from app.api.dependencies.db import get_db
from app.api.dependencies.user import get_current_user
from app.schemas.resource.resource import ResourceInfo, ResourceCreate
from app.services.resource.resource import resource_service

router = APIRouter()


@router.get("/resource/{resource_id}")
async def get_file_by_id(resource_id: int, db=Depends(get_db)):
    return await resource_service.get_one(db, resource_id)


@router.get("/resource/info/{resource_id}", response_model=ResourceInfo)
async def get_resource_info(resource_id: int, db=Depends(get_db), token=Depends(get_current_user)):
    return await resource_service.get_one_info(db, resource_id)


@router.post("/resources", status_code=status.HTTP_201_CREATED)
async def upload_files(files: List[ResourceCreate], project_id: Optional[int] = None, event_id: Optional[int] = None,
                       db=Depends(get_db), token=Depends(get_current_user)):
    await resource_service.upload(db, files, project_id, event_id)


@router.delete("/resource/{resource_id}")
async def delete_file(resource_id: int, db=Depends(get_db), token=Depends(get_current_user)):
    return await resource_service.delete(db, resource_id)

