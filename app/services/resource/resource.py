import base64
import os
import pathlib
import uuid
from typing import List, Optional
import aiofiles
from aiofiles import os as aos

from fastapi import HTTPException
from fastapi.responses import StreamingResponse

from app.core.config import settings
from app.repositories.resource.resource import ResourceRepository
from app.services.resource.extension import extension_service
from app.services.resource.type import type_service
from app.repositories.entity.project import ProjectRepository
from app.repositories.entity.event import EventRepository
from app.repositories.user.user import UserRepository
from app.schemas.resource.resource import ResourceInfo, ResourceCreate, Resource
from app.schemas.resource.image import Image, ImageCreate
from app.api.error.base import HTTPExceptionNotSupported, HTTPExceptionNotFound


class ResourceService:
    def __init__(self):
        if not os.path.exists(settings.COMMON_FILE_PATH):
            os.makedirs(settings.COMMON_FILE_PATH)

    @staticmethod
    async def get_one(db, resource_id: int):
        resource_repo = ResourceRepository(db)
        resource_record = await resource_repo.get_one(resource_id)
        if resource_record is None:
            raise HTTPExceptionNotFound.resource(resource_id)
        extension_model = await extension_service.get_one(db, resource_record["extension_id"])

        async def iterator():
            async with aiofiles.open(resource_record["path"], "rb") as f:
                while chunk := await f.read(1024):
                    yield chunk
        return StreamingResponse(iterator(), media_type=extension_model.media_type)

    async def get_one_info(self, db, resource_id: int):
        resource_repo = ResourceRepository(db)
        resource_record = await resource_repo.get_one(resource_id)
        if resource_record is None:
            raise HTTPExceptionNotFound.resource(resource_id)
        return await self.create_model_resource_info(db, resource_record)

    async def get_by_project_id(self, db, project_id: int, limit: int = 10):
        resource_repo = ResourceRepository(db)
        resource_records = await resource_repo.get_by_project_id(project_id, limit)
        return await self.create_model_resources(db, resource_records)

    async def get_by_event_id(self, db, event_id: int):
        resource_repo = ResourceRepository(db)
        return await resource_repo.get_image_by_event_id(event_id)

    async def get_images_by_project_id(self, db, project_id: int, limit: int = 10):
        resource_repo = ResourceRepository(db)
        resource_records = await resource_repo.get_images_by_project_id(project_id, limit)
        return await self.create_model_images(db, resource_records)

    async def get_image_by_user(self, db, user_id: int):
        resource_repo = ResourceRepository(db)
        resource_record = await resource_repo.get_image_by_user(user_id)
        if resource_record is not None:
            return await self.create_model_image(db, resource_record)

    async def update_image(self, db, images: List[ImageCreate], project_id: Optional[int] = None,
                           event_id: Optional[int] = None, user_id: Optional[int] = None):
        await self.delete_images(db, project_id=project_id, event_id=event_id, user_id=user_id)
        await self.upload_image(db, images, project_id=project_id, event_id=event_id, user_id=user_id)

    async def delete_images(self, db, project_id: Optional[int] = None,
                           event_id: Optional[int] = None, user_id: Optional[int] = None):
        event_repo = EventRepository(db)
        resource_repo = ResourceRepository(db)
        resources = []
        try:
            # Удаляем изображения из проекта
            if project_id is not None:
                raise NotImplementedError('Удаление файлов для проекта не реализованно')

            # Удаляем изображения из эвента
            if event_id is not None:
                resources = [await resource_repo.get_image_by_event_id(event_id)]
                if not len(resources):
                    return

                await resource_repo.delete_event_images(event_id)

            # Удаляем изображения из юзера
            if user_id is not None:
                raise NotImplementedError('Удаление файлов для юзера не реализованна ')

            [await aos.remove(resource["path"]) for resource in resources]

        except HTTPException as e:
            for resource in resources:
                await aos.remove(resource)
            raise e
    async def upload_image(self, db, images: List[ImageCreate], project_id: Optional[int] = None,
                           event_id: Optional[int] = None, user_id: Optional[int] = None):
        resource_repo = ResourceRepository(db)
        project_repo = ProjectRepository(db)
        event_repo = EventRepository(db)
        user_repo = UserRepository(db)
        resources = []
        try:
            for image in images:
                file_part = image.file.split('base64,')
                if len(file_part) != 2:
                    raise Exception
                extension_mn = pathlib.Path(image.filename).suffix
                extension_model = await extension_service.get_by_extension(db, extension_mn)

                if extension_model is None:
                    raise HTTPExceptionNotSupported.extension(extension_mn)

                type_model = await type_service.get_by_extension(db, extension_model.mn)
                if type_model is None:
                    raise Exception
                if type_model.name != 'image':
                    raise Exception

                resource_id, save_path = await self.save_file(db, file_part[1], image.filename, extension_model)
                resources.append(save_path)

                # Связываем изображение с проектом
                if project_id is not None:
                    if not await project_repo.exists(project_id):
                        raise HTTPExceptionNotFound.project(project_id)
                    await resource_repo.attach_image_to_project(resource_id, project_id)

                # Связываем изображение с событием
                if event_id is not None:
                    if not await event_repo.exists(event_id):
                        raise HTTPExceptionNotFound.event(event_id)
                    await resource_repo.attach_image_to_event(resource_id, event_id)

                if user_id is not None:
                    if not await user_repo.exists(user_id):
                        raise HTTPExceptionNotFound.user()
                    await resource_repo.attach_image_to_user(resource_id, user_id)

        except HTTPException as e:
            for resource in resources:
                await aos.remove(resource)
            raise e

    async def upload(self, db, files: List[ResourceCreate], project_id: Optional[int] = None,
                     event_id: Optional[int] = None):
        resource_repo = ResourceRepository(db)
        project_repo = ProjectRepository(db)
        event_repo = EventRepository(db)
        resources = []
        try:
            for file in files:
                file_part = file.file.split('base64,')
                if len(file_part) != 2:
                    raise Exception

                extension_mn = pathlib.Path(file.filename).suffix
                extension_model = await extension_service.get_by_extension(db, extension_mn)

                if extension_model is None:
                    raise HTTPExceptionNotSupported.extension(extension_mn)

                resource_id, save_path = await self.save_file(db, file_part[1], file.filename, extension_model)
                resources.append(save_path)
                # Связываем ресурс с проектом
                if project_id is not None:
                    if not await project_repo.exists(project_id):
                        raise HTTPExceptionNotFound.project(project_id)
                    await resource_repo.attach_to_project(resource_id, project_id)

                # Связываем ресурс с событием
                if event_id is not None:
                    if not await event_repo.exists(event_id):
                        raise HTTPExceptionNotFound.event(event_id)
                    await resource_repo.attach_to_event(resource_id, event_id)
        except HTTPException as e:
            for resource in resources:
                await aos.remove(resource)
            raise e

    @staticmethod
    async def save_file(db, file, filename, extension):
        resource_repo = ResourceRepository(db)
        uuid_resource_name = f'{str(uuid.uuid4())}{extension.mn}'
        save_path = f'{settings.COMMON_FILE_PATH}/{uuid_resource_name}'

        async with aiofiles.open(save_path, "w+b") as f:
            await f.write(base64.b64decode(str.encode(file)))

        resource_id = await resource_repo.insert(extension.id, save_path, filename)
        return resource_id, save_path

    @staticmethod
    async def delete(db, resource_id: int):
        resource_repo = ResourceRepository(db)
        resource_model = await resource_repo.get_one(resource_id)
        if resource_model is None:
            raise HTTPExceptionNotFound.resource(resource_id)

        await resource_repo.delete(resource_id)
        if os.path.exists(resource_model.path):
            await aos.remove(resource_model.path)

    @staticmethod
    async def delete_user_image(db, user_id: int):
        resource_repo = ResourceRepository(db)
        await resource_repo.delete_user_image(user_id)

    async def create_model_resources(self, db, resource_records):
        return [await self.create_model_resource(db, record) for record in resource_records]

    @staticmethod
    async def create_model_resource(db, resource_record):
        return Resource(id=resource_record["id"])

    async def create_model_images(self, db, resource_records):
        return [await self.create_model_image(db, record) for record in resource_records]

    @staticmethod
    async def create_model_image(db, resource_record):
        return Image(id=resource_record["id"])

    @staticmethod
    async def create_model_resource_info(db, resource_record):
        extension = await extension_service.get_one(db, resource_record["extension_id"])
        type_ = await type_service.get_by_extension(db, extension.name)
        return ResourceInfo(id=resource_record["id"],
                            original_name=resource_record["original_name"],
                            type=type_,
                            extension=extension)


resource_service = ResourceService()
