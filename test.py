import asyncio

from refactor.base.db import async_session
from refactor.classes.crud import ClassesCRUD
from refactor.classes.handlers import scrape_spreadsheet
from refactor.google_api.crud import GoogleApiCRUD
from refactor.google_api.handlers import GoogleApiHandler


async def test():
    db = ClassesCRUD(async_session)
    # results = await scrape_spreadsheet()
    await db.empty_table()
    # for res in results:
    #     await db.create(**res.dict())


asyncio.run(test())
