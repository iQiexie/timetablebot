from app.frontend.clients.backend import BackendApi
from config import settings


class RequestClients:
    vk_backend = BackendApi(token=settings.VK_BACKEND_SECRET_KEY)
    tg_backend = BackendApi(token=settings.TG_BACKEND_SECRET_KEY)
