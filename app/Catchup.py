import json

import vk_api
import ast
from app.Assets.Filters import today, tomorrow
from app.ClassProcessor import ClassProcessor
from app.Database import Database

MAIN_TOKEN = open('secret/tokenmain', 'r').read()  # домашка
SCHEDULE_TOKEN = open('secret/token', 'r').read()  # расписание
MPSU_TOKEN = open('secret/tokenmpsu', 'r').read()  # расписание

vk_session = vk_api.VkApi(token=MPSU_TOKEN)
vk = vk_session.get_api()


def check_today(message: str) -> bool:
    message = message.lower()
    if "пары" in message or "список" in message or "расписание" in message:
        if "сёдня" in message or "седня" in message or "сегодня" in message:
            return True


def check_tomorrow(message: str) -> bool:
    message = message.lower()
    if "пары" in message or "список" in message or "расписание" in message:
        if "завтра" in message:
            return True


class UnprocessedMessage:
    message: str
    payload: dict
    user_id: int

    def __init__(self, message, user_id, payload):
        self.message = message
        self.user_id = user_id
        self.payload = payload

    def __repr__(self):
        return "(" \
               f"user_id={self.user_id}" \
               f", payload={self.payload}" \
               f", message={self.message}" \
               ")"


def get_unanswered_messages():
    query = vk_session.method("messages.getDialogs", {"unanswered": "1"})
    dialogs = query.get("items")

    messages = []

    for dialog in dialogs:
        messages.append(UnprocessedMessage(
            message=dialog.get("message").get("body"),
            payload=dialog.get("message").get("payload"),
            user_id=dialog.get("message").get("user_id")
        ))

    return messages


def identify_intent(message: UnprocessedMessage) -> UnprocessedMessage:
    if check_tomorrow(message.message):
        message.payload = {"command": "today"}
    elif check_today(message.message):
        message.payload = {"command": "tomorrow"}
    elif not message.payload:
        message.payload = {}
    else:
        message.payload = json.loads(str(message.payload))
        print(message.payload)

    return message


def process_messages():
    unprocessed_messages = get_unanswered_messages()
    processed_messages = []
    for message in unprocessed_messages:
        processed_messages.append(identify_intent(message))

    return unprocessed_messages


def run_catchup():
    report = ""

    messages = process_messages()
    for message in messages:
        command = message.payload.get("command")
        group_id = Database(message.user_id).get_group_index()
        cp = ClassProcessor(group_index=group_id)

        if command == "today":
            sending_message = cp.get_today()
        elif command == "tomorrow":
            sending_message = cp.get_tomorrow()
        else:
            sending_message = "None"

        print(f"----------------------------------{command}------------------------------------------")
        print(sending_message)

        # TODO разобраться с show day. Потому что щас я беру только команду из  payload, а там ещё другие штуки есть
        # TODO