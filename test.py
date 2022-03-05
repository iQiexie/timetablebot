import asyncio

from refactor.base.db import async_session
from refactor.google_api.crud import GoogleApiCRUD
from refactor.google_api.handlers import GoogleApiHandler


async def test_driver():
    google = GoogleApiHandler(GoogleApiCRUD(async_session))
    return await google.create_service(
        'drive',
        'v2',
        ['https://www.googleapis.com/auth/drive']
    )


async def test_sheets():
    google = GoogleApiHandler(GoogleApiCRUD(async_session))
    return await google.create_service(
        'sheets',
        'v4',
        ['https://www.googleapis.com/auth/spreadsheets.readonly']
    )


async def test():
    driver = await test_driver()
    sheets = await test_sheets()
    print(driver, sheets)


asyncio.run(test())
