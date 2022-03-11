import asyncio

from refactor.backend.base.db import async_session
from refactor.backend.classes.crud import ClassesCRUD
from refactor.backend.classes.handlers import scrape_spreadsheet


# TODO получать инфу о том, когда была обновлена бд, можно по created_at у рандомной пары


async def test():
    db = ClassesCRUD(async_session)
    results = await scrape_spreadsheet()
    # await db.empty_table()
    for res in results:
        await db.create(**res.dict())
    res = await db.get(208, 2, False)
    for r in res:
        print(r)

asyncio.run(test())
