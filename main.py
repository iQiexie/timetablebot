from app.vk_bot.driver import start_production_bot, start_stage_bot
from config import settings

if __name__ == '__main__':
    if settings.PRODUCTION:
        start_production_bot()
    else:
        start_stage_bot()
