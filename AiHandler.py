import requests
import urllib.parse
from requests.structures import CaseInsensitiveDict

url = "http://p-bot.ru/api/getAnswer"
headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json; charset=utf-8"


def get_response(input_message):
    payload = {'request': input_message}
    request_message = urllib.parse.urlencode(payload).replace('+', "%20")
    request = request_message + "&request_1=&answer_1=&request_2=&answer_2=&request_3=&answer_3=&bot_name=%CF%81Bot&user_name=%D0%9D%D0%B5%D0%B7%D0%BD%D0%B0%D0%BA%D0%BE%D0%BC%D0%B5%D1%86&dialog_lang=ru&dialog_id=fdce304b-1858-4772-ac5c-3d7cd290d04c&dialog_greeting=false&a=public-api&b=3662261068&c=1951488886&d=2576866283&e=0.9856392031850265&t=1634978131943&x=6.566398771590876"

    response = requests.post(url, headers=headers, data=request).json()
    return response['answer']
