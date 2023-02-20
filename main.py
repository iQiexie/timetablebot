import os
import asyncio
from app.routines import actualize
from app.routines import count_users
from app.vk_bot.driver import run

if __name__ == "__main__":
    if os.getenv("ROUTINE") == "ACTUALIZE":
        asyncio.run(actualize())
    elif os.getenv("ROUTINE") == "REPORT":
        asyncio.run(count_users())
    else:
        run()
