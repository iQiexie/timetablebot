import asyncio
import time
import traceback
from app.backend.classes.crud import ClassesREDIS

redis = ClassesREDIS()


async def try_wrapper():
    try:
        await redis.reset_database()
        await asyncio.sleep(3600)
    except Exception as e:
        print(f"Actualizer failed: {e}")
        traceback.print_exc()

asyncio.run(redis.reset_database())
