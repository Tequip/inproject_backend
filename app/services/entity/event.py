from app.api.error.base import HTTPExceptionNotFound
from app.repositories.entity.category import CategoryRepository
from app.repositories.entity.event import EventRepository
from app.repositories.entity.location import LocationRepository
from app.repositories.entity.tag import TagRepository
from app.schemas.entity.event.event import Event
from app.schemas.entity.event.event_related import EventRelated
from app.schemas.entity.event.event_short import EventShort
from app.schemas.resource.image import Image
from app.services.entity.category import category_service
from app.services.entity.location import location_service
from app.services.entity.tag import tag_service
from app.services.resource.resource import resource_service
from app.services.user import user_service


async def get_event_locations(db, event_id):
    return await location_service.get_by_event_id(db, event_id)


class EventService:
    def __init__(self):
        pass

    @staticmethod
    async def exists(db, event_id: int):
        event_repo = EventRepository(db)
        return await event_repo.exists(event_id)

    async def update_event(self, db, event_to_update: Event, user):
        event_repo = EventRepository(db)
        event_exists = await event_repo.exists(event_to_update.id)
        if not event_exists:
            raise HTTPExceptionNotFound.event(event_to_update.id)
        await event_repo.update(event_to_update)

        await self.update_event_locations(db, event_to_update.id, event_to_update.locations)
        await self.update_event_tags(db, event_to_update.id, event_to_update.tags)
        await self.update_event_categories(db, event_to_update.id, event_to_update.categories)

        await resource_service.update_image(db, [event_to_update.title_photo], event_id=event_to_update.id)

    async def create_event(self, db, event_to_create: Event, user):
        event_repo = EventRepository(db)
        e_id = await event_repo.create(event_to_create)
        created_event_id = int(**e_id)

        await self.update_event_locations(db, created_event_id, event_to_create.locations)
        await self.update_event_tags(db, created_event_id, event_to_create.tags)
        await self.update_event_categories(db, created_event_id, event_to_create.categories)

        await resource_service.upload_image(db, event_to_create.title_photo, event_id=created_event_id)

    async def get_one_by_id(self, db, event_id) -> Event:
        event_repo = EventRepository(db)
        event = await event_repo.get_one(event_id)
        if event is None:
            raise HTTPExceptionNotFound.event(event_id)

        return await self.create_model_event(db, event)

    async def create_model_event(self, db, event) -> Event:
        image = await self.get_event_image(db, event["id"])
        tags = await self.get_event_tags(db, event["id"])
        categories = await self.get_event_categories(db, event["id"])
        locations = await get_event_locations(db, event["id"])
        owner = await user_service.get_short_one(db, event["owner_id"])
        related_events = await self.get_related_events_by_event(db, event["id"])

        return Event(id=event["id"],
                     name=event["title"],
                     about=event["about"],
                     start_date=event["start_date"],
                     end_date=event["end_date"],
                     created_date=event["created"],
                     is_hidden=event["is_hidden"],
                     source_url=event["source_url"],
                     title_photo=image,
                     locations=locations,
                     categories=categories,
                     tags=tags,
                     owner=owner,
                     related_events=related_events
                     )

    async def create_model_short_event(self, db, event):
        image = await self.get_event_image(db, event["id"])
        tags = await self.get_event_tags(db, event["id"])
        categories = await self.get_event_categories(db, event["id"])
        locations = await get_event_locations(db, event["id"])
        return EventShort(id=event["id"],
                          name=event["title"],
                          short_about=event["short_about"],
                          title_photo=image,
                          locations=locations,
                          categories=categories,
                          tags=tags
                          )

    async def create_models_related_events(self, db, events):
        return [await self.create_model_related_event(db, event) for event in events]

    async def create_model_related_event(self, db, event):
        image = await self.get_event_image(db, event["id"])
        return EventRelated(id=event["id"],
                            name=event["title"],
                            title_photo=image
                            )

    async def get_many_by_query_location_category(self, db, query, location, category, limit, page):
        event_repo = EventRepository(db)
        events_ids = set()
        if limit is None:
            limit = 10
        if page is None:
            page = 0

        if query is not None:
            events_ids.update(set(await event_repo.get_by_query(query)))
        if location is not None:
            events_ids.update(set(await event_repo.get_by_location(location.lower().split(','))))
        if category is not None:
            events_ids.update(set(await event_repo.get_by_category(category.lower().split(','))))

        if query is None and location is None and category is None:
            events = await event_repo.all(limit, page)
        else:
            events = await event_repo.get_many([event_id for event_id in events_ids], limit, page)

        return await self.create_model_events(db, events)

    async def create_model_events(self, db, events):
        return [await self.create_model_short_event(db, event) for event in events]

    async def get_event_image(self, db, event_id):
        img_record = await resource_service.get_by_event_id(db, event_id)
        if img_record is None:
            return None
        return self.create_model_image(img_record)

    async def get_event_tags(self, db, event_id):
        return await tag_service.get_by_event_id(db, event_id)

    async def get_event_categories(self, db, event_id):
        return await category_service.get_by_event_id(db, event_id)

    async def get_event_owner(self, db, owner_id):
        return await user_service.get_short_one(db, owner_id)

    async def get_related_events_by_event(self, db, event_id):
        event_repo = EventRepository(db)
        events_ids = await event_repo.get_related_events(event_id)
        events = await event_repo.get_many(events_ids)
        return await self.create_models_related_events(db, events)

    async def update_event_locations(self, db, event_id, locations):
        location_repo = LocationRepository(db)
        current_locations = await location_service.get_by_event_id(db, event_id)
        locations_id = [location.id for location in locations]
        for_insert = set(locations_id).difference(set(location.id for location in current_locations))
        for_delete = set(location.id for location in current_locations).difference(set(locations_id))
        if len(for_insert):
            await location_repo.insert_event_locations(event_id, list(for_insert))
        if len(for_delete):
            await location_repo.delete_event_locations(event_id, list(for_delete))

    async def update_event_tags(self, db, event_id, tags):
        tag_rep = TagRepository(db)
        current_tags = await tag_service.get_by_event_id(db, event_id)
        tags_id = [tag.id for tag in tags]
        for_insert = set(tags_id).difference(set(tag.id for tag in current_tags))
        for_delete = set(tag.id for tag in current_tags).difference(set(tags_id))
        if len(for_insert):
            await tag_rep.insert_event_tags(event_id, list(for_insert))
        if len(for_delete):
            await tag_rep.delete_event_tags(event_id, list(for_delete))

    async def update_event_categories(self, db, event_id, categories):
        category_repo = CategoryRepository(db)
        current_categories = await category_repo.get_by_event_id(event_id)
        categories_id = [cat["id"] for cat in categories]
        for_insert = set(categories_id).difference(set(tag.id for tag in current_categories))
        for_delete = set(tag.id for tag in current_categories).difference(set(categories_id))
        if len(for_insert):
            await category_repo.insert_event_categories(event_id, list(for_insert))
        if len(for_delete):
            await category_repo.delete_event_categories(event_id, list(for_delete))

    def create_model_image(self, img_record):
        return Image(id=img_record["id"])


event_service = EventService()
