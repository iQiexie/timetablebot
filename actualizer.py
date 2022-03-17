import asyncio
import multiprocessing as mp
from multiprocessing import freeze_support

from app.backend.classes.crud import ClassesREDIS


async def run():
    redis = ClassesREDIS()
    await redis.reset_database()


def main():
    freeze_support()
    asyncio.run(run())


if __name__ == '__main__':
    q = mp.Queue()
    p = mp.Process(target=main)
    p.start()
    print(q.get())
    p.join()
