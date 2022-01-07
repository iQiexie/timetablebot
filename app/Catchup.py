import json

import vk_api
from vk_api import ApiError
from app.ClassProcessor import ClassProcessor
from app.Database import Database

MAIN_TOKEN = open('secret/tokenmain', 'r').read()  # домашка
SCHEDULE_TOKEN = open('secret/token', 'r').read()  # расписание
MPSU_TOKEN = open('secret/tokenmpsu', 'r').read()  # расписание

vk_session = vk_api.VkApi(token=SCHEDULE_TOKEN)
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

    return message


def process_messages():
    unprocessed_messages = get_unanswered_messages()
    processed_messages = []
    for message in unprocessed_messages:
        processed_messages.append(identify_intent(message))

    return unprocessed_messages


def send_message(text: str, user_id: int):
    vk_session.method("messages.send", {
        "user_id": user_id,
        "message": text,
        "random_id": 0
    })


def run_catchup():
    report = "Report:"
    messages = process_messages()

    for message in messages:
        command = message.payload.get("command")
        group_id = Database(message.user_id).get_group_index()
        cp = ClassProcessor(group_index=group_id)

        if not command:
            continue

        if command == "today":
            sending_message = cp.get_today()
        elif command == "tomorrow":
            sending_message = cp.get_tomorrow()
        elif command == "show day":
            sending_message = cp.getByDay(message.payload.get("day"), message.payload.get('next week'))
        else:
            sending_message = None

        try:
            if sending_message:
                send_message(sending_message, message.user_id)
                report += f"\nSuccessfully sent: {message.user_id}"
                print(f"Responding to: {message.message} $$$ With {command}")
        except ApiError as e:
            report += f"\n {message.user_id} Failed due to {e}"

    send_message(report, 232444433)


# TODO добавить свитч токенов
# TODO добавить свитч unanswered, unread в get_unanswered_messages
