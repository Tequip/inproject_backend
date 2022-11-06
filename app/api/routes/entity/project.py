from typing import Optional, List
from fastapi import APIRouter, Depends
from app.api.dependencies.db import get_db
from app.api.dependencies.user import get_current_user
from app.services.entity.project import project_service
from app.services.entity.category import category_service
from app.schemas.entity.project.project_short import ProjectShort, Page
from app.schemas.entity.project.project import Project, ProjectCreate
from app.schemas.user.user import UserShort
from app.schemas.entity.category import PredictCategory


router = APIRouter()


@router.get("/projects", response_model=Page)
async def get_project(query: Optional[str] = None, location: Optional[str] = None,
                      category: Optional[str] = None, page: Optional[int] = None,
                      limit: Optional[int] = None, db=Depends(get_db), token=Depends(get_current_user)):
    return await project_service.get_many_by_query_location_category(db, token.user_id, query,
                                                                     location, category, page, limit)


@router.get("/projects/popular", response_model=List[ProjectShort])
async def get_popular_projects(limit: Optional[int] = 10, db=Depends(get_db), token=Depends(get_current_user)):
    return await project_service.get_popylar(db, limit)


@router.get("/project/{project_id}/like", response_model=List[UserShort])
async def get_project_like(project_id: int, db=Depends(get_db), token=Depends(get_current_user)):
    return await project_service.get_by_project_like(db, project_id, token.user_id)


@router.post("/project/{project_id}/like")
async def create_project_like(project_id: int, db=Depends(get_db), token=Depends(get_current_user)):
    return await project_service.create_like(db, project_id, token.user_id)


@router.delete("/project/{project_id}/like")
async def delete_project_like(project_id: int, db=Depends(get_db), token=Depends(get_current_user)):
    return await project_service.delete_like(db, project_id, token.user_id)


@router.get("/project/{project_id}/predict_category", response_model=List[PredictCategory])
async def get_predict_category(project_id: int, db=Depends(get_db), token=Depends(get_current_user)):
    return await category_service.get_predict_by_project(db, project_id)


@router.get("/project/{project_id}", response_model=Project)
async def get_project_by_id(project_id: int, db=Depends(get_db), token=Depends(get_current_user)):
    return await project_service.get_one(db, project_id, token.user_id)


@router.post("/project", response_model=Project)
async def create_project(project: ProjectCreate, db=Depends(get_db), token=Depends(get_current_user)):
    return await project_service.create(db, project, token.user_id)
