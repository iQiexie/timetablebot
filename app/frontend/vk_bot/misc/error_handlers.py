import logging
import traceback

from vkbottle import BaseMiddleware
from vkbottle import ErrorHandler

from config import settings

error_handler = ErrorHandler(redirect_arguments=True, raise_exceptions=True)


@error_handler.register_undefined_error_handler
async def exc_handler_undefined(e: Exception, *args) -> None:
    middleware: BaseMiddleware = args[0]
    logging.info(f"Oh no! {args} returned an error. \n\nTraceback:")
    tb_str = ";".join(traceback.format_exception(None, e, e.__traceback__))
    logging.info(tb_str)

    if isinstance(middleware, BaseMiddleware):
        await middleware.event.answer(tb_str)
