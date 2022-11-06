from app.db.connection import engine


async def get_db():
    async with engine.begin() as connection:
        yield connection
