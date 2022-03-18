import asyncio
import multiprocessing as mp
from multiprocessing import freeze_support

from app.backend.classes.crud import ClassesREDIS
from app.backend.classes.handlers import scrape_spreadsheet


async def run():
    redis = ClassesREDIS()

    while True:
        day_schemas = await scrape_spreadsheet()
        await redis.reset_database(day_schemas)
        await asyncio.sleep(3600)


def main():
    freeze_support()
    asyncio.run(run())


if __name__ == '__main__':
    q = mp.Queue()
    p = mp.Process(target=main)
    p.start()
    print(q.get())
    p.join()
