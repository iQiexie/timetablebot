from aiogram import Dispatcher

from app.frontend.tg_bot.handlers.classes import class_search_router
from app.frontend.tg_bot.handlers.feedback import feedback_router
from app.frontend.tg_bot.handlers.menu import initial_router
from app.frontend.tg_bot.handlers.settings import settings_router
from app.frontend.tg_bot.middlewares.auth import AuthMiddleware
from app.frontend.tg_bot.middlewares.error import ErrorMiddleware


def setup_message_middlewares(dispatcher: Dispatcher) -> None:
    dispatcher.message.middleware(ErrorMiddleware())
    dispatcher.message.middleware(AuthMiddleware())


def setup_query_middlewares(dispatcher: Dispatcher) -> None:
    dispatcher.callback_query.middleware(ErrorMiddleware())
    dispatcher.callback_query.middleware(AuthMiddleware())


def get_root_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    setup_message_middlewares(dispatcher)
    setup_query_middlewares(dispatcher)

    dispatcher.include_router(initial_router)
    dispatcher.include_router(class_search_router)
    dispatcher.include_router(feedback_router)
    dispatcher.include_router(settings_router)

    return dispatcher
