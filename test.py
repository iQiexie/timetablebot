import asyncio

from refactor.base.db import async_session
from refactor.classes.crud import ClassesCRUD
from refactor.classes.handlers import scrape_spreadsheet
from refactor.google_api.crud import GoogleApiCRUD
from refactor.google_api.handlers import GoogleApiHandler


async def test():
    await scrape_spreadsheet(ClassesCRUD(async_session))


asyncio.run(test())
