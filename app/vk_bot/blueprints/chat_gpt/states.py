from vkbottle import BaseStateGroup


class ChatGptStates(BaseStateGroup):
    CHATTING = "CHATTING"
    WAITING_FOR_ANSWER = "WAITING_FOR_ANSWER"
    NOT_CHATTING = "NOT_CHATTING"
