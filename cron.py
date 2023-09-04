import os

import requests

from config import settings

r = requests.request(
    method=os.getenv("METHOD"),
    url="http://localhost:8000/api" + os.getenv("URL"),
    headers={"Authorization": f"Bearer {settings.ADMIN_SECRET_KEY}"},
)

print(r.text)
