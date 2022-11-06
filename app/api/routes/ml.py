from fastapi import APIRouter
from app.core.celery_app import relation_project, recommendation_users_and_projects, project_predict_category

router = APIRouter()


@router.get("/relation_project")
async def root():
    relation_project.delay()
    return {"message": "Start ML!"}


@router.get("/recommendation_users_and_projects")
async def ml_2():
    recommendation_users_and_projects.delay()
    return {"message": "Start ML!"}


@router.get("/project_predict_category")
async def ml_3():
    project_predict_category.delay()
    return {"message": "Start ML!"}
