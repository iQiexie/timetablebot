from vkwave.bots import SimpleLongPollBot, SimpleBotEvent, PayloadFilter, BotEvent, PayloadContainsFilter
from vkwave.bots.fsm import FiniteStateMachine, StateFilter, ForWhat, State

from Assets import Keyboards
from Database import Database
from ClassProcessor import ClassProcessor

main_id = open('secret/token', 'r').read()  # Токен паблика бота
main_group_id = 198604544  # Айди паблика бота

bot = SimpleLongPollBot(tokens=main_id, group_id=main_group_id)
fsm = FiniteStateMachine()

group_index = State("group_index")  # это нужно для fsm

DEFAULT_ANSWER = 'Ok'


def get_group_index(event):
    return Database(event.peer_id).get_group_index()


# ... Cоздание бд для беседы, инициализация ...
@bot.message_handler(bot.text_contains_filter("старт"))
async def start(event: SimpleBotEvent):
    Database(event.peer_id)
    await event.answer(keyboard=Keyboards.main().get_keyboard(), message=DEFAULT_ANSWER)


# ... Сегодняшние пары ...
@bot.message_handler(PayloadFilter({"command": "today"}))
async def today(event: SimpleBotEvent):
    cp = ClassProcessor(get_group_index(event))

    await event.answer(message=cp.getByDay(1))


# ... Настройки ...
@bot.message_handler(PayloadFilter({"command": "settings"}))
async def settings(event: SimpleBotEvent):
    text = "Ваша группа: " + str(get_group_index(event))
    await event.answer(message=text, keyboard=Keyboards.settings().get_keyboard())


# начало интервью
@bot.message_handler(PayloadFilter({"command": "change group"}))
async def new_index(event: BotEvent):
    await fsm.set_state(event=event, state=group_index, for_what=ForWhat.FOR_CHAT)
    return "Напишите мне новый номер группы"


# конец интервью и получение индекса
@bot.message_handler(StateFilter(fsm=fsm, state=group_index, for_what=ForWhat.FOR_CHAT), )
async def new_index(event: BotEvent):
    if not event.object.object.message.text.isdigit():
        return f"Мне нужны только циферки!"
    await fsm.add_data(
        event=event,
        for_what=ForWhat.FOR_CHAT,
        state_data={"group_index": event.object.object.message.text},
    )
    user_data = await fsm.get_data(event=event, for_what=ForWhat.FOR_CHAT)

    await fsm.finish(event=event, for_what=ForWhat.FOR_CHAT)

    # всё выше - получение индекса. Индекс получен

    Database(event.object.object.message.peer_id).update_group_index(user_data['group_index'])

    return f"Ваша новая группа: {user_data['group_index']}"


# ... Дебаг ...

@bot.message_handler(bot.text_contains_filter("qwe"))
async def dev(event: SimpleBotEvent):
    cp = ClassProcessor(get_group_index(event))

    await event.answer(message=str(cp.getByDay()))


# ... Расписание ...
@bot.message_handler(PayloadFilter({"command": "this week"}))
async def timetable(event: SimpleBotEvent):
    await event.answer(message=DEFAULT_ANSWER, keyboard=Keyboards.week().get_keyboard())


@bot.message_handler(PayloadFilter({"command": "next week"}))
async def timetable(event: SimpleBotEvent):
    await event.answer(message=DEFAULT_ANSWER, keyboard=Keyboards.week_next().get_keyboard())


@bot.message_handler(PayloadContainsFilter("show day"))
async def timetable(event: SimpleBotEvent):
    await event.answer(message=str(event.payload))


# ... Навигация ...
@bot.message_handler(PayloadFilter({"command": "kill keyboard"}))
async def navigation(event: SimpleBotEvent):
    await event.answer(message=DEFAULT_ANSWER)


@bot.message_handler(PayloadFilter({"command": "main menu"}))
async def navigation(event: SimpleBotEvent):
    await event.answer(message=DEFAULT_ANSWER, keyboard=Keyboards.main().get_keyboard())


print("started")
bot.run_forever()
