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
from app.schemas.entity.news import NewsCreate
from app.services.entity.news import news_service


router = APIRouter()


@router.post("/news", response_model=Page)
async def get_project(news: NewsCreate, db=Depends(get_db), token=Depends(get_current_user)):
    return await news_service.create(db, news, token.user_id)