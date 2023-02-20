import os
import asyncio

from app.backend.handlers.classes.main import update_classes
from app.vk_bot.driver import run

if __name__ == "__main__":
    if os.getenv("ROUTINE") == "ACTUALIZE":
        asyncio.run(update_classes())
    else:
        run()
