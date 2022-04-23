from apscheduler.schedulers.blocking import BlockingScheduler

from app.backend.classes.crud import ClassesREDIS
from app.backend.classes.handlers import scrape_spreadsheet

redis = ClassesREDIS()


async def run():
    print('UPDATING!!!')
    day_schemas = await scrape_spreadsheet()
    await redis.reset_database(day_schemas)

scheduler = BlockingScheduler(timezone='UTC', daemon=True)
scheduler.add_job(run, 'interval', minutes=60, max_instances=1)

scheduler.start()
