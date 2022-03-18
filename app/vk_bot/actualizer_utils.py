import asyncio
from multiprocessing import freeze_support

from app.backend.classes.crud import ClassesREDIS
from app.backend.classes.handlers import scrape_spreadsheet

redis = ClassesREDIS()


async def __class_updater_util():
    day_schemas = await scrape_spreadsheet()
    await redis.reset_database(day_schemas)


def class_updater():
    freeze_support()
    asyncio.run(__class_updater_util())
