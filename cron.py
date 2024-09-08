import os
from datetime import datetime

import requests

from config import settings

r = requests.request(
    method=os.getenv("METHOD"),
    url=settings.BACKEND_BASE_URL_SWAGGER + os.getenv("URL"),
    headers={"Authorization": f"Bearer {settings.TG_BACKEND_SECRET_KEY}"},
)

print(f"{datetime.now()} - {r.text}")  # noqa
