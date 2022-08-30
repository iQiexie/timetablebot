import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.backend.classes.crud import ClassesREDIS
from app.backend.classes.handlers import scrape_spreadsheet


async def update():
    redis = ClassesREDIS()
    day_schemas = await scrape_spreadsheet()
    await redis.reset_database(day_schemas)


scheduler = AsyncIOScheduler(timezone='UTC', daemon=True)
scheduler.add_job(update, 'interval', seconds=30)
scheduler.start()

asyncio.get_event_loop().run_forever()
