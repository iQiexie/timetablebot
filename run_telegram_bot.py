import asyncio

from app.frontend.tg_bot.main import start_telegram_bot


async def main() -> None:
    await start_telegram_bot()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
