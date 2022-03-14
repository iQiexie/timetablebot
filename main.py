from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.backend.classes.crud import ClassesREDIS
from app.vk_bot.driver import start_production_bot, start_stage_bot

redis = ClassesREDIS()
scheduler = AsyncIOScheduler(timezone="UTC", daemon=True)
scheduler.add_job(redis.reset_database, 'interval', hours=1, max_instances=1)

if __name__ == '__main__':
    start_production_bot()
    # start_stage_bot()
