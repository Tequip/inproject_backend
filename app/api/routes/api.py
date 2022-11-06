from fastapi import APIRouter
from app.api.routes import home, ml
from app.api.routes.resource import resource
from app.api.routes.auth import internal, swagger
from app.api.routes.user import user, interest, skill
from app.api.routes.entity import project, category, location, tag, stage, news, event

router = APIRouter()
router.include_router(home.router, tags=["home"])
router.include_router(swagger.router, tags=["swagger"], prefix="/swagger")
router.include_router(internal.router, tags=["auth"])
router.include_router(skill.router, tags=["user"], prefix="/user")
router.include_router(interest.router, tags=["user"], prefix="/user")
router.include_router(user.router, tags=["user"])
router.include_router(project.router, tags=["project"])
router.include_router(news.router, tags=["project"])
router.include_router(ml.router, tags=["ml"])
router.include_router(resource.router, tags=["resource"])
router.include_router(category.router, tags=["entity"], prefix="/entity")
router.include_router(location.router, tags=["entity"], prefix="/entity")
router.include_router(tag.router, tags=["entity"], prefix="/entity")
router.include_router(stage.router, tags=["entity"], prefix="/entity")
router.include_router(event.router, tags=["event"])
