import requests
import urllib.parse
from requests.structures import CaseInsensitiveDict


def get_headers(content_type):
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = content_type

    return headers


def make_pbot_request(input_message, creds):
    payload = {
        'request': input_message,
        'request_1': "",
        'answer_1': "",
        'request_2': "",
        'answer_2': "",
        'request_3': "",
        'answer_3': "",
        'bot_name': "Олексей Поликарпович",
        'user_name': "Незнакомец",
        'dialog_lang': "ru",
        'dialog_id': "fdce304b-1858-4772-ac5c-3d7cd290d04c",
        'dialog_greeting': "false"
    }

    request = urllib.parse.urlencode(payload).replace('+', "%20") + creds
    response = requests.post("http://p-bot.ru/api/getAnswer",
                             headers=get_headers("application/json; charset=utf-8"),
                             data=request)

    if response.status_code == 200:
        return response.json()['answer']
    else:
        return None


def make_aiproject_request(input_message, userid):
    payload = {
        "ask": {"ask": input_message},
        "userid": {"userid": userid},
    }

    ask = urllib.parse.urlencode(payload['ask']).replace('+', "%20").split("=")[1]
    userid = urllib.parse.urlencode(payload['userid']).replace('+', "%20").split("=")[1]
    data = f"query=%7B%22ask%22%3A%22{ask}%22%2C%22userid%22%3A%22{userid}%22%2C%22key%22%3A%22%22%7D"
    response = requests.post("https://aiproject.ru/api/",
                             headers=get_headers("application/x-www-form-urlencoded"),
                             data=data)

    if response.status_code == 200:
        return response.json()['aiml'].encode('l1').decode()
    else:
        return None


def make_roughs_request(input_message):
    return requests.get(f"https://roughs.ru/api/talker?text={input_message}&source_from=test@test.ru").json()['answer']


class Ai_Handler:
    def __init__(self):
        self.__creds = "&a=public-api&b=2274607559&c=3910293392&d=1317267059" \
                       "&e=0.043848485432916195&t=1635075420985&x=1.043045154172797"

    def update_creds(self, new_creds):
        self.__creds = new_creds

    def get_response(self, input_message, userid):
        pbot_response = make_pbot_request(input_message, self.__creds)
        if pbot_response:
            return pbot_response

        aiproject_response = make_aiproject_request(input_message, userid)
        if aiproject_response:
            return aiproject_response

        return make_roughs_request(input_message)