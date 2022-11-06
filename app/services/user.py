from app.repositories.user.user import UserRepository
from app.repositories.user.auth import AuthRepository
from app.services.security import security_service
from app.core.config import settings
from app.schemas.user.user import User, UserShort
from app.schemas.user.auth import Login
from app.api.error.base import HTTPExceptionAlreadyExists, HTTPExceptionNotFound, \
    HTTPExceptionCloseRegistration, HTTPExceptionAuth
from app.services.resource.resource import resource_service
from app.services.skill import skill_service
from app.services.interest import interest_service
from typing import List


class UserService:
    def __init__(self):
        pass

    @staticmethod
    async def login(db, email, password):
        user_repo = UserRepository(db)
        user_id = await user_repo.exists_by_email(email)
        if user_id is None:
            raise HTTPExceptionNotFound.user()

        auth_repo = AuthRepository(db)
        hashed_password = await auth_repo.get_hashed_password(user_id)
        if not security_service.verify_password(password, hashed_password[0]):
            raise HTTPExceptionAuth.bad_credential()

        tokens = security_service.create_key_pair(payload={"user_id": user_id})
        user = await user_repo.get_one(user_id)
        return Login(**tokens, user=user, is_admin=user["is_admin"])

    @staticmethod
    async def create(db, user):
        if not settings.OPEN_REGISTRATION:
            raise HTTPExceptionCloseRegistration()

        user_repo = UserRepository(db)
        user_id = await user_repo.exists_by_email(user.email)
        if user_id is not None:
            raise HTTPExceptionAlreadyExists.user()

        user_id = await user_repo.create(user)
        auth_repo = AuthRepository(db)
        await auth_repo.create(user_id["id"], security_service.hashing_password(user.password))

        tokens = security_service.create_key_pair(payload={"user_id": user_id["id"]})
        user = await user_repo.get_one(user_id["id"])
        return Login(**tokens, user=user, is_admin=user["is_admin"])

    async def get_one(self, db, user_id, requesting_user_id: int):
        user_repo = UserRepository(db)
        user_record = await user_repo.get_one(user_id)
        if user_record is None:
            raise HTTPExceptionNotFound.user()
        return await self.create_user(db, user_record, requesting_user_id)

    async def get_short_one(self, db, user_id):
        user_repo = UserRepository(db)
        user_record = await user_repo.get_one(user_id)
        if user_record is None:
            raise HTTPExceptionNotFound.user()
        return await self.create_short_user(db, user_record)

    async def get_short_many(self, db, user_ids):
        user_repo = UserRepository(db)
        user_record = await user_repo.get_many(user_ids)
        return await self.create_short_users(db, user_record)

    async def get_short_by_project(self, db, project_id: int):
        user_repo = UserRepository(db)
        user_ids = await user_repo.get_by_project(project_id)
        users = await user_repo.get_many(user_ids)
        return await self.create_short_users(db, users)

    async def get_short_recommended_by_project(self, db, project_id: int):
        user_repo = UserRepository(db)
        user_ids = await user_repo.get_short_recommended_by_project(project_id)
        users = await user_repo.get_many(user_ids)
        return await self.create_short_users(db, users)

    async def update(self, db, user_id, user_model):
        user_repo = UserRepository(db)
        if user_model.photo is not None:
            await resource_service.delete_user_image(db, user_id)
            await resource_service.upload_image(db, [user_model.photo], user_id=user_id)
        await self.update_user_skill(db, user_id, user_model.skill)
        await self.update_user_interest(db, user_id, user_model.interest)
        user_id = await user_repo.update(user_id, user_model)
        return await self.get_one(db, user_id["id"], user_id["id"])

    async def all(self, db):
        user_repo = UserRepository(db)
        user_records = await user_repo.all()
        return await self.create_short_users(db, user_records)

    @staticmethod
    async def update_user_skill(db, user_id: int, skill_ids: List[int]):
        user_repo = UserRepository(db)
        skills = await skill_service.get_by_user(db, user_id)
        for_insert = set(skill_ids).difference(set(skill.id for skill in skills))
        for_delete = set(skill.id for skill in skills).difference(set(skill_ids))
        if len(for_insert):
            await user_repo.insert_user_skill(user_id, list(for_insert))
        if len(for_delete):
            await user_repo.delete_user_skill(user_id, list(for_delete))

    @staticmethod
    async def update_user_interest(db, user_id: int, interest_ids: List[int]):
        user_repo = UserRepository(db)
        interests = await interest_service.get_by_user(db, user_id)
        for_insert = set(interest_ids).difference(set(interest.id for interest in interests))
        for_delete = set(interest.id for interest in interests).difference(set(interest_ids))
        if len(for_insert):
            await user_repo.insert_user_interest(user_id, list(for_insert))
        if len(for_delete):
            await user_repo.delete_user_interest(user_id, list(for_delete))

    async def create_short_users(self, db, user_records):
        return [await self.create_short_user(db, user_record) for user_record in user_records]

    @staticmethod
    async def create_short_user(db, user_record):
        photo = await resource_service.get_image_by_user(db, user_record["id"])
        photo_url = None
        if photo is not None:
            photo_url = photo.url
        return UserShort(id=user_record["id"],
                         first_name=user_record["first_name"],
                         last_name=user_record["last_name"],
                         telegram=user_record["telegram"],
                         about=user_record["about"],
                         status=user_record["status"],
                         role=user_record["role"],
                         photo=photo_url,
                         email=user_record["email"])

    async def create_users(self, db, user_records, requesting_user_id):
        return [await self.create_user(db, user_record, requesting_user_id) for user_record in user_records]

    @staticmethod
    async def create_user(db, user_record, requesting_user_id):
        # TODO перекрестный импорт пофиксить
        from app.services.entity.project import project_service
        photo = await resource_service.get_image_by_user(db, user_record["id"])
        photo_url = None
        if photo is not None:
            photo_url = photo.url
        skills = await skill_service.get_by_user(db, user_record["id"])
        interests = await interest_service.get_by_user(db, user_record["id"])
        project_creator = await project_service.get_short_by_owner(db, user_record["id"], requesting_user_id)
        project_member = await project_service.get_short_by_member(db, user_record["id"], requesting_user_id)
        project_liked = await project_service.get_short_by_user_like(db, user_record["id"], requesting_user_id)
        project_recommended = await project_service.get_short_recommended_by_user(db, user_record["id"])
        return User(photo=photo_url,
                    id=user_record["id"],
                    telegram=user_record["telegram"],
                    about=user_record["about"],
                    status=user_record["status"],
                    role=user_record["role"],
                    email=user_record["email"],
                    skill=skills,
                    interest=interests,
                    project_creator=project_creator,
                    project_member=project_member,
                    project_liked=project_liked,
                    project_recommended=project_recommended,
                    is_admin=user_record["is_admin"]
                    )


user_service = UserService()
