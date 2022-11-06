from sqlalchemy import select

from app.models.resource.resource import resource_table, a_resource_event_table, \
    a_resource_project_table, a_image_project_table, a_image_event_table, a_image_user_table
from app.repositories.base import BaseRepository


class ResourceRepository(BaseRepository):
    def __init__(self, connection):
        super(ResourceRepository, self).__init__(connection, resource_table)

    async def get_by_project_id(self, project_id: int, limit: int):
        query = select([resource_table]).select_from(
            resource_table.join(a_resource_project_table)
        ).where(a_resource_project_table.c.project_id == project_id).limit(limit)
        records = await self.connection.execute(query)
        return records.fetchall()

    async def get_images_by_project_id(self, project_id: int, limit: int):
        query = select([resource_table]).select_from(
            resource_table.join(a_image_project_table)
        ).where(a_image_project_table.c.project_id == project_id).limit(limit)
        records = await self.connection.execute(query)
        return records.fetchall()

    async def get_image_by_user(self, user_id: int):
        query = select([resource_table]).select_from(
            resource_table.join(a_image_user_table)
        ).where(a_image_user_table.c.user_id == user_id).limit(1)
        records = await self.connection.execute(query)
        return records.fetchone()

    async def get_by_event_id(self, event_id: int, limit: int = 10):
        query = select([resource_table]).select_from(
            resource_table.join(a_resource_event_table)
        ).where(a_resource_event_table.c.event_id == event_id).limit(limit)
        records = await self.connection.execute(query)
        return records.fetchall()

    async def get_image_by_event_id(self, event_id: int):
        query = select([resource_table]).select_from(
            resource_table.join(a_image_event_table)
        ).where(a_image_event_table.c.event_id == event_id)
        records = await self.connection.execute(query)
        return records.fetchone()

    async def insert(self, extension_id: int, save_path: str, original_name: str) -> int:
        query = resource_table.insert().values(extension_id=extension_id,
                                               path=save_path,
                                               original_name=original_name).returning(resource_table.c.id)
        record = await self.connection.execute(query)
        return record.fetchone()["id"]

    async def attach_to_project(self, resource_id: int, project_id: int) -> None:
        query = a_resource_project_table.insert().values(resource_id=resource_id, project_id=project_id)
        await self.connection.execute(query)

    async def attach_to_event(self, resource_id: int, event_id: int) -> None:
        query = a_resource_event_table.insert().values(resource_id=resource_id, event_id=event_id)
        await self.connection.execute(query)

    async def attach_image_to_project(self, resource_id: int, project_id: int) -> None:
        query = a_image_project_table.insert().values(resource_id=resource_id, project_id=project_id)
        await self.connection.execute(query)

    async def attach_image_to_event(self, resource_id: int, event_id: int) -> None:
        query = a_image_event_table.insert().values(resource_id=resource_id, event_id=event_id)
        await self.connection.execute(query)

    async def attach_image_to_user(self, resource_id: int, user_id: int) -> None:
        query = a_image_user_table.insert().values(resource_id=resource_id, user_id=user_id)
        await self.connection.execute(query)

    async def delete(self, resource_id: int) -> None:
        query = resource_table.delete().where(resource_table.c.id == resource_id)
        await self.connection.execute(query)

    async def delete_event_images(self, event_id):
        query = a_resource_event_table.delete().where(a_resource_event_table.c.event_id == event_id)
        await self.connection.execute(query)

    async def delete_user_image(self, user_id: int) -> None:
        query = a_image_user_table.delete().where(a_image_user_table.c.user_id == user_id)
        await self.connection.execute(query)
