from typing import List, Optional
import math
from app.repositories.entity.project import ProjectRepository
from app.schemas.entity.project.project_short import ProjectShort, Page
from app.schemas.entity.project.project import Project, ProjectCreate
from app.services.entity.tag import tag_service
from app.services.entity.category import category_service
from app.services.entity.location import location_service
from app.services.user import user_service
from app.services.resource.resource import resource_service
from app.api.error.base import HTTPExceptionNotFound, HTTPExceptionPermission
from app.schemas.entity.project.member import MemberCreate
from app.services.entity.member import member_service
from app.services.entity.stage import stage_service
from app.services.entity.news import news_service


class ProjectService:
    def __init__(self):
        pass

    async def get_one(self, db, project_id, user_id):
        project_repo = ProjectRepository(db)
        project_record = await project_repo.get_one(project_id)
        if project_record is None:
            raise HTTPExceptionNotFound.project(project_id)
        if project_record["is_hidden"]:
            if project_record["owner_id"] != user_id:
                raise HTTPExceptionPermission.project(project_id)
        return await self.create_model_project(db, project_record, user_id)

    async def get_many_by_query_location_category(self, db, user_id: int, query: Optional[str], location: Optional[str],
                                                  category: Optional[str], page: Optional[int], limit: Optional[int]):
        project_repo = ProjectRepository(db)
        projects_id = set()
        if query is not None:
            projects_id.update(set(await project_repo.get_by_query(query)))
        if location is not None:
            projects_id.update(set(await project_repo.get_by_location(location.lower().split(','))))
        if category is not None:
            projects_id.update(set(await project_repo.get_by_category(category.lower().split(','))))

        if query is None and location is None and category is None:
            projects_ids = [project.id for project in await project_repo.all()]
            if limit is None:
                limit = 10

            if page is not None:
                projects = await project_repo.get_many(projects_ids[(page-1)*limit:page*limit], user_id, limit)
            else:
                projects = await project_repo.get_many(projects_ids, user_id, limit)

            max_page = math.ceil(len(projects_ids) / limit)
        else:
            if limit is None:
                limit = 10

            if page is not None:
                projects = await project_repo.get_many([project_id for project_id in projects_id[(page-1)*limit:page*limit]], user_id, limit)
            else:
                projects = await project_repo.get_many(
                    [project_id for project_id in projects_id], user_id, limit)
            max_page = math.ceil(len(projects_id))

        project_models = await self.create_model_short_projects(db, projects)
        return Page(projects=project_models, current_page=page, max_page=max_page)

    async def get_short_recommended_by_user(self, db, user_id: int):
        project_repo = ProjectRepository(db)
        project_ids = await project_repo.get_short_recommended_by_user(user_id)
        projects = await project_repo.get_many(project_ids)
        return await self.create_model_short_projects(db, projects)

    async def get_popylar(self, db, limit: int):
        project_repo = ProjectRepository(db)
        project_ids = await project_repo.get_by_like(limit)
        projects = await project_repo.get_many(project_ids)
        return await self.create_model_short_projects(db, projects)

    async def get_short_relation_project_by_project(self, db, project_id: int, user_id: int):
        project_repo = ProjectRepository(db)
        project_ids = await project_repo.get_relation_project(project_id)
        projects = await project_repo.get_many(project_ids, user_id)
        return await self.create_model_short_projects(db, projects)

    async def get_short_by_owner(self, db, user_id: int, requesting_user_id: int, limit: int = 30):
        project_repo = ProjectRepository(db)
        project_ids = await project_repo.get_by_owner(user_id, limit)
        project_records = await project_repo.get_many(project_ids, requesting_user_id)
        return await self.create_model_short_projects(db, project_records)

    async def get_short_by_member(self, db, user_id: int, requesting_user_id: int, limit: int = 30):
        project_repo = ProjectRepository(db)
        project_ids = await project_repo.get_by_member(user_id, limit)
        project_records = await project_repo.get_many(project_ids, requesting_user_id)
        return await self.create_model_short_projects(db, project_records)

    async def get_short_by_user_like(self, db, user_id: int, requesting_user_id: int,  limit: int = 30):
        project_repo = ProjectRepository(db)
        project_ids = await project_repo.get_by_user_like(user_id, limit)
        project_records = await project_repo.get_many(project_ids, requesting_user_id)
        return await self.create_model_short_projects(db, project_records)

    @staticmethod
    async def get_by_project_like(db, project_id, requesting_user_id):
        project_repo = ProjectRepository(db)
        user_ids = await project_repo.get_by_project_like(project_id, requesting_user_id)
        return await user_service.get_short_many(db, user_ids)

    @staticmethod
    async def create_like(db, project_id, user_id):
        project_repo = ProjectRepository(db)
        project_record = await project_repo.get_one(project_id)
        if project_record is None:
            raise HTTPExceptionNotFound.project(project_id)

        if project_record["is_hidden"]:
            is_member = await project_repo.is_owner(project_id, user_id)
            is_owner = await project_repo.is_member(project_id, user_id)
            if not (is_owner or is_member):
                raise HTTPExceptionPermission.project(project_id)

        await project_repo.create_like(project_id, user_id)

    @staticmethod
    async def delete_like(db, project_id, user_id):
        project_repo = ProjectRepository(db)
        await project_repo.delete_like(project_id, user_id)

    @staticmethod
    async def exists(db, project_id: int):
        project_repo = ProjectRepository(db)
        return await project_repo.exists(project_id)

    async def create(self, db, project_model: ProjectCreate, user_id):
        project_repo = ProjectRepository(db)
        project_id = await project_repo.create(project_model)

        await resource_service.upload_image(db, project_model.images, project_id)
        await self.update_project_location(db, project_id, project_model.locations)
        await self.update_project_tag(db, project_id, project_model.tags)
        await self.update_project_category(db, project_id, project_model.categories)
        await self.update_project_member(db, project_id, project_model.members)
        project_record = await project_repo.get_one(project_id)
        return await self.create_model_project(db, project_record, user_id)

    @staticmethod
    async def update_project_location(db, project_id: int, location_ids: List[int]):
        project_repo = ProjectRepository(db)
        locations = await location_service.get_by_project_id(db, project_id)
        for_insert = set(location_ids).difference(set(location.id for location in locations))
        for_delete = set(location.id for location in locations).difference(set(location_ids))
        if len(for_insert):
            await project_repo.insert_project_location(project_id, list(for_insert))
        if len(for_delete):
            await project_repo.delete_project_location(project_id, list(for_delete))

    @staticmethod
    async def update_project_category(db, project_id: int, category_ids: List[int]):
        project_repo = ProjectRepository(db)
        categories = await category_service.get_by_project_id(db, project_id)
        for_insert = set(category_ids).difference(set(category.id for category in categories))
        for_delete = set(category.id for category in categories).difference(set(category_ids))
        if len(for_insert):
            await project_repo.insert_project_category(project_id, list(for_insert))
        if len(for_delete):
            await project_repo.delete_project_category(project_id, list(for_delete))

    @staticmethod
    async def update_project_tag(db, project_id: int, tag_ids: List[int]):
        project_repo = ProjectRepository(db)
        tags = await tag_service.get_by_project_id(db, project_id)
        for_insert = set(tag_ids).difference(set(tag.id for tag in tags))
        for_delete = set(tag.id for tag in tags).difference(set(tag_ids))
        if len(for_insert):
            await project_repo.insert_project_tag(project_id, list(for_insert))
        if len(for_delete):
            await project_repo.delete_project_tag(project_id, list(for_delete))

    @staticmethod
    async def update_project_member(db, project_id: int, member_models: List[MemberCreate]):
        members = await member_service.get_by_project_id(db, project_id)
        for_delete = set(member.user_id for member in members).difference(set(member.user_id for member in member_models))
        if len(for_delete):
            await member_service.update_remove_status(db, project_id, list(for_delete))
        await member_service.upsert(db, project_id, member_models)

    async def create_model_short_projects(self, db, projects):
        return [await self.create_model_short_project(db, project) for project in projects]

    @staticmethod
    async def create_model_short_project(db, project):
        images = await resource_service.get_images_by_project_id(db, project["id"], limit=1)
        image = None
        if len(images):
            image = images[0].url
        tags = await tag_service.get_by_project_id(db, project["id"])
        category = await category_service.get_by_project_id(db, project["id"])
        location = await location_service.get_by_project_id(db, project["id"])
        return ProjectShort(id=project["id"],
                            title=project["title"],
                            image=image,
                            about=project["short_about"],
                            tags=tags,
                            categories=category,
                            locations=location,
                            created=project["created"],
                            likes=project["likes"])

    async def create_model_project(self, db, project, user_id):
        images = await resource_service.get_images_by_project_id(db, project["id"])
        tags = await tag_service.get_by_project_id(db, project["id"])
        category = await category_service.get_by_project_id(db, project["id"])
        location = await location_service.get_by_project_id(db, project["id"])
        owner = await user_service.get_short_one(db, project["owner_id"])
        members = await member_service.get_by_project_id(db, project["id"])
        related_projects = await self.get_short_relation_project_by_project(db, project["id"], user_id)
        stage = None
        if project["stage_id"] is not None:
            stage = await stage_service.get_one(db, project["stage_id"])
        user_recommended = await user_service.get_short_recommended_by_project(db, project["id"])
        news = await news_service.get_by_project(db, project["id"])
        return Project(id=project["id"],
                       images=images,
                       title=project["title"],
                       about=project["about"],
                       tags=tags,
                       categories=category,
                       locations=location,
                       created=project["created"],
                       deadline=project["deadline"],
                       likes=project["likes"],
                       is_hidden=project["is_hidden"],
                       stage=stage.name,
                       owner=owner,
                       members=members,
                       is_project_owner=True if user_id == owner.id else False,
                       is_project_member=True if user_id in [member.user.id for member in members] else False,
                       related_projects=related_projects,
                       user_recommended=user_recommended,
                       news=news
                       )


project_service = ProjectService()
