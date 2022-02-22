# import vk_api
# import glob
#
#
# class VkGroup:
# 	def __init__(self, token):
# 		self.__vk_api = vk_api.VkApi(token=token)
#
# 	def send_message(self, id, text):
# 		self.__vk_api.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})
#
#
# domashka = VkGroup(
# "efa8f72bc9f5aab07245dbc8eb42f58551b1c56be06fc8ac549a92db582a9dfbd6866d44351067cd08534")
# raspisanie = VkGroup(
# "86cb2d37e043794bf720c51415f267f6bcab2ac3e66eca28a092458d9baf6cff692595321a09cb4fed5bb")
# mpgu = VkGroup(
# "a3608f75ac2a4cd423e8551853c7f1348bc94f3de8fa4b7509f28c9ac63ad00e05abcebe2defb874416aa")
#
# msg = """
# [Автоматическая рассылка сообщений]
# Новое расписание теперь доступно в боте. Для начала работы с ботом напиши "старт"
#
# Подробнее: https://vk.com/wall-152158632_4651
# """
#
# users_raw = glob.glob("*.db")
# users = []
# for user in users_raw:
# 	user_id = user.split('.')[0]
#
# 	try:
# 		raspisanie.send_message(user_id, msg)
# 	except Exception as e:
# 		print(f"For: {user_id} Caught: {e}")
# 	else:
# 		print(f"Sent to: {user_id}")

import vk_api

SCHEDULE_TOKEN = \
    '86cb2d37e043794bf720c51415f267f6bcab2ac3e66eca28a092458d9baf6cff692595321a09cb4fed5bb'  #
# расписание
vk_session = vk_api.VkApi(token=SCHEDULE_TOKEN)
vk = vk_session.get_api()


def send_message(text: str, user_id: int):
    vk_session.method(
        "messages.send", {
            "user_id": user_id,
            "message": text,
            "random_id": 0
        }
    )


def get_ids():
    query = vk_session.method("messages.getDialogs", {"count": 60})
    dialogs = query.get("items")

    user_ids = [dialog.get("message").get("user_id") for dialog in dialogs]
    print(user_ids)

    return user_ids


ids = get_ids()

for id in ids:
    pass
    # print(f"sending to: https://vk.com/id{id}")
    # send_message(
    #     "У бота сломався сервер на хостинге, но самый крутой в мире Админ-мэн всё "
    #     "починил, больше ломаться не должно", id
    #     )
