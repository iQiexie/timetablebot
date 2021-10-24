import requests
import urllib.parse
from requests.structures import CaseInsensitiveDict

url = "http://p-bot.ru/api/getAnswer"
headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json; charset=utf-8"


class Ai_Handler:
    def __init__(self):
        self.__creds = "&a=public-api&b=2274607559&c=3910293392&d=1317267059" \
                       "&e=0.043848485432916195&t=1635075420985&x=1.043045154172797"

    def update_creds(self, new_creds):
        self.__creds = new_creds

    def get_response(self, input_message):
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

        request = urllib.parse.urlencode(payload).replace('+', "%20") + self.__creds
        response_raw = requests.post(url, headers=headers, data=request)

        if response_raw.status_code == 200:
            response = response_raw.json()
        else:
            response = requests.get(f"https://roughs.ru/api/talker?text={input_message}"
                                    f"&source_from=test@test.ru").json()

        return response['answer']
