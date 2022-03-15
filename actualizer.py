import asyncio
import time
from app.backend.classes.crud import ClassesREDIS

redis = ClassesREDIS()


async def try_wrapper():
    try:
        await redis.reset_database()
        time.sleep(3600)
    except Exception as e:
        print(f"Actualizer failed: {e}")

    return try_wrapper()


while True:
    asyncio.run(try_wrapper())
