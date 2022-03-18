import asyncio
from app.backend.google_api.handlers import GoogleApiHandler


async def run():
    google = GoogleApiHandler()
    await google.init_services()
    await google.update_credentials()

asyncio.run(run())
