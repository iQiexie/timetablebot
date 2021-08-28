from vkwave.bots import SimpleLongPollBot, SimpleBotEvent, PayloadFilter, BotEvent, PayloadContainsFilter, \
    TextContainsFilter, ClonesBot
from vkwave.bots.fsm import FiniteStateMachine, StateFilter, ForWhat, State

from Assets import Keyboards
from Database import Database
from ClassProcessor import ClassProcessor

main_id = open('secret/token', 'r').read()  # Токен паблика бота
main_group_id = 206763355  # Айди паблика бота

bot = SimpleLongPollBot(tokens=main_id, group_id=main_group_id)
fsm = FiniteStateMachine()

group_index = State("group_index")  # это нужно для fsm
DEFAULT_ANSWER = 'Oк'

today_filters = (
        (
                TextContainsFilter('бот') & TextContainsFilter('пары') &
                (TextContainsFilter('сёдня') | TextContainsFilter('седня'))
        ) |
        PayloadFilter({"command": "today"})
)

tomorrow_filters = (
        (
                TextContainsFilter('бот') & TextContainsFilter('пары') & TextContainsFilter('завтра')
        ) |
        PayloadFilter({"command": "tomorrow"})
)

start_filters = (
        TextContainsFilter('старт') |
        TextContainsFilter('привет') |
        TextContainsFilter('start') |
        TextContainsFilter('покежь клаву') |
        TextContainsFilter('клава')
)


def get_group_index(event):
    return Database(event.peer_id).get_group_index()


# ... Cоздание бд для беседы, инициализация ...
@bot.message_handler(start_filters)
async def start(event: SimpleBotEvent):
    Database(event.peer_id)
    await event.answer(keyboard=Keyboards.main().get_keyboard(), message=DEFAULT_ANSWER)


# ... Сегодняшние и Завтрашние пары ...
@bot.message_handler(today_filters)
async def today(event: SimpleBotEvent):
    cp = ClassProcessor(get_group_index(event))

    await event.answer(message=cp.get_today(), keyboard=Keyboards.main().get_keyboard())


@bot.message_handler(tomorrow_filters)
async def today(event: SimpleBotEvent):
    cp = ClassProcessor(get_group_index(event))

    await event.answer(message=cp.get_tomorrow(), keyboard=Keyboards.main().get_keyboard())


# ... Настройки ...
@bot.message_handler(PayloadFilter({"command": "settings"}))
async def settings(event: SimpleBotEvent):
    text = f"Ваша группа: " + str(get_group_index(event))
    text += "\nЕсли чё-то не работает, пиши мне @baboomka"
    text += "\n\nБыстрый доступ:"
    text += "\n1. Если в теле сообщения содержатся слова (Старт, привет, клава, start, покежь клаву) - открывает меню"
    text += "\n2. Если в теле сообщения содержатся слова (бот, пары, сёдня) - отправляет список пар на сегодня"
    text += "\n3. Если в теле сообщения содержатся слова (бот, пары, завтра) - отправляет список пар на завтра"
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
    await event.answer(message=event.text)


# ... Расписание ...
@bot.message_handler(PayloadFilter({"command": "this week"}))
async def timetable(event: SimpleBotEvent):
    await event.answer(message=DEFAULT_ANSWER, keyboard=Keyboards.week().get_keyboard())


@bot.message_handler(PayloadFilter({"command": "next week"}))
async def timetable(event: SimpleBotEvent):
    await event.answer(message=DEFAULT_ANSWER, keyboard=Keyboards.week_next().get_keyboard())


@bot.message_handler(PayloadContainsFilter("show day"))
async def timetable(event: SimpleBotEvent):
    payload = event.payload
    cp = ClassProcessor(get_group_index(event))

    if payload['next week']:
        await event.answer(message=cp.getByDay(payload['day'], True))
    else:
        await event.answer(message=cp.getByDay(payload['day']))

    # await event.answer(message=str(payload))


# ... Навигация ...
@bot.message_handler(PayloadFilter({"command": "kill keyboard"}))
async def navigation(event: SimpleBotEvent):
    await event.answer(message=DEFAULT_ANSWER)


@bot.message_handler(PayloadFilter({"command": "main menu"}))
async def navigation(event: SimpleBotEvent):
    await event.answer(message=DEFAULT_ANSWER, keyboard=Keyboards.main().get_keyboard())


token2 = open('secret/tokenmain', 'r').read()
clones = ClonesBot(
    bot,
    SimpleLongPollBot(tokens=token2, group_id=198604544)
)

print("started")
clones.run_all_bots()
