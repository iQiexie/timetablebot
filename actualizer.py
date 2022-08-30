import asyncio

from app.backend.classes.crud import ClassesREDIS
from app.backend.classes.handlers import scrape_spreadsheet

redis = ClassesREDIS()


async def update():
    day_schemas = await scrape_spreadsheet()
    await redis.reset_database(day_schemas)


asyncio.run(update())