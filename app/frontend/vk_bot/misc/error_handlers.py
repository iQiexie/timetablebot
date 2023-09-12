import logging
import traceback

import aiohttp
from vkbottle import BaseMiddleware, ErrorHandler

from config import settings

error_handler = ErrorHandler(redirect_arguments=True, raise_exceptions=True)


@error_handler.register_undefined_error_handler
async def exc_handler_undefined(e: Exception, *args, **kwargs) -> None:
    middleware: BaseMiddleware = args[0]

    error_msg = f"{args=}, {kwargs=} Oh no! returned an error. \n\nTraceback:"
    logging.info(error_msg)

    tb_str = ";".join(traceback.format_exception(None, e, e.__traceback__))
    logging.info(tb_str)

    request_kwargs = dict(
        method="GET",
        url=f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage",
        params={"chat_id": settings.TELEGRAM_ALERTS_CHAT_ID, "text": f"{error_msg}\n{tb_str}"},
    )

    async with aiohttp.ClientSession() as session:
        async with session.request(**request_kwargs):
            pass

    if isinstance(middleware, BaseMiddleware):
        await middleware.event.answer(tb_str)
