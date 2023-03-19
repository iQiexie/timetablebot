import os
import asyncio
from app.routines import actualize
from app.routines import count_users
from app.vk_bot.driver import run
from config import settings

if __name__ == "__main__":
    if os.getenv("ROUTINE") == "ACTUALIZE":
        print(f"Running actualize routine with {settings.PRODUCTION=}")
        asyncio.run(actualize())
    elif os.getenv("ROUTINE") == "REPORT":
        print(f"Running report routine with {settings.PRODUCTION=}")
        asyncio.run(count_users())
    else:
        print(f"Starting bot with {settings.PRODUCTION=}")
        run()
