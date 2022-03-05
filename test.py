import asyncio

from refactor.base.db import async_session
from refactor.google_api.crud import GoogleApiCRUD
from refactor.google_api.handlers import GoogleApiHandler


async def test():
    service = await google.create_service(
    'sheets',
    'v4',
    ['https://www.googleapis.com/auth/spreadsheets.readonly']
)
    print(service)

google = GoogleApiHandler(GoogleApiCRUD(async_session))
asyncio.run(test())
