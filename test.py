import time

import requests
from random import randint
from config import settings


def send_message(message: str, peer_ids: list[int]):
    r = requests.post(
        "https://api.vk.com/method/messages.send",
        data={
            "access_token": settings.RASPISANIE_TOKEN,
            "peer_ids": peer_ids,
            "message": message,
            "random_id": randint(1, 1000),
            "attachment": "photo-206763355_457239386,photo-206763355_457239387",
            "v": 5.131,
         },
    )

    print(r.text)


def get_conversations(count: int, offset: int):
    r = requests.post(
        "https://api.vk.com/method/messages.getConversations",
        data={
            "access_token": settings.RASPISANIE_TOKEN,
            "count": count,
            "offset": offset,
            "v": 5.131,
        }
    )

    result = []
    items = r.json()['response']['items']
    for item in items:
        id_ = item['conversation']['peer']['id']
        result.append(id_)

    print(result)
    return result


res1 = get_conversations(count=200, offset=0)
res2 = get_conversations(count=100, offset=200)
peer_ids = res1 + res2

message = (
    "Всем привет!\n\n"
    "Бот был заблокирован компанией, у которой арендуется сервер. "
    "Причина блокировки надумана и админу неясна. Бот уже работает, а хостинг сменён.\n\n"
    "Простите за неудобства, админ не ломал пентагон, честно-честно 🥺👉👈\n\n"
    "Подробнее: https://vk.com/mpsu_schedule?w=wall-206763355_195"
)

for i in peer_ids:
    time.sleep(1)
    send_message(message=message, peer_ids=[i])
