from app.frontend.vk_bot.middlewares.auth import AuthMiddleware
from app.frontend.vk_bot.middlewares.no_bot import NoBotMiddleware

middlewares = [
    AuthMiddleware,
    NoBotMiddleware,
]
