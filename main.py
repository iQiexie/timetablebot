from apscheduler.schedulers.asyncio import AsyncIOScheduler

from refactor.backend.classes.crud import ClassesREDIS
from refactor.vk_bot.driver import start_bot

redis = ClassesREDIS()
scheduler = AsyncIOScheduler(timezone="UTC", daemon=True)
scheduler.add_job(redis.reset_database, 'interval', hours=1, max_instances=1)

if __name__ == '__main__':
    # TODO мигрировать пользователей из старой бд в эту новую
    start_bot()
