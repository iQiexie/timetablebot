from vkwave.bots import SimpleLongPollBot, SimpleBotEvent, BotEvent, ClonesBot, PayloadContainsFilter, MiddlewareResult
from vkwave.bots.fsm import FiniteStateMachine, StateFilter, ForWhat, State

from Assets import Keyboards, Filters, Strings
from Database import Database
from ClassProcessor import ClassProcessor
from SheetScraper import update_spreadsheet, delete_spreadsheet

from threading import Timer
from datetime import datetime


MAIN_TOKEN = open('secret/tokenmain', 'r').read()  # домашка
MAIN_GROUP_ID = 198604544  # домашка

SCHEDULE_TOKEN = open('secret/token', 'r').read()  # расписание
SCHEDULE_GROUP_ID = 206763355  # расписание

MPSU_TOKEN = open('secret/tokenmpsu', 'r').read()  # расписание
MPSU_GROUP_ID = 152158632  # расписание

GROUP_INDEX = State("group_index")  # это нужно для fsm

bot = SimpleLongPollBot(tokens=MAIN_TOKEN, group_id=MAIN_GROUP_ID)
new_bot = SimpleLongPollBot(tokens=SCHEDULE_TOKEN, group_id=SCHEDULE_GROUP_ID)
mpsu_bot = SimpleLongPollBot(tokens=MPSU_TOKEN, group_id=MPSU_GROUP_ID)

fsm = FiniteStateMachine()

CLONES = ClonesBot(
    bot,  # домашка
    # new_bot,  # расписание
    # mpsu_bot
)

current_spreadsheet = {
    "id": None,
    "updated_time": ""
}


def spreadsheet_updating_service():
    if current_spreadsheet['id'] is not None:
        delete_spreadsheet(current_spreadsheet['id'])

    current_spreadsheet['id'] = update_spreadsheet()
    current_spreadsheet['updated_time'] = datetime.now().strftime('%H:%M')

    Timer(3600, spreadsheet_updating_service).start()


spreadsheet_updating_service()


def get_group_index(event):
    return Database(event.peer_id).get_group_index()


def reply_allowed(peer_id, message) -> bool:
    return Filters.group_message(peer_id, message) or Filters.dm_message(peer_id)


@bot.middleware()
@new_bot.middleware()
async def check(event: SimpleBotEvent) -> MiddlewareResult:
    # Middleware - это глобальный фильтр. Если он вернёт False, все остальные фильтры забракуются

    if event.object.type == "message_new":
        peer_id = event.object.object.message.peer_id
        message = event.object.object.message.text

        if reply_allowed(peer_id, message):
            return MiddlewareResult(True)

    return MiddlewareResult(False)


# ... Cоздание бд для беседы, инициализация ...
@bot.message_handler(Filters.start)
async def group_messages(event: SimpleBotEvent):
    Database(event.peer_id)
    await event.answer(keyboard=Keyboards.main().get_keyboard(), message=Strings.DEFAULT_ANSWER_MESSAGE)


# ... Сегодняшние и Завтрашние пары ...
@bot.message_handler(Filters.today)
async def today(event: SimpleBotEvent):
    cp = ClassProcessor(get_group_index(event))
    await event.answer(message=cp.get_today(), keyboard=Keyboards.main().get_keyboard())


@bot.message_handler(Filters.tomorrow)
async def today(event: SimpleBotEvent):
    cp = ClassProcessor(get_group_index(event))
    await event.answer(message=cp.get_tomorrow(), keyboard=Keyboards.main().get_keyboard())


# ... Настройки ...
@bot.message_handler(Filters.settings)
async def settings(event: SimpleBotEvent):
    await event.answer(message=Strings.Settings(get_group_index(event)),
                       keyboard=Keyboards.settings().get_keyboard())


@bot.message_handler(Filters.last_update_time)
async def uptime(event: SimpleBotEvent):

    await event.answer(message=Strings.Spreadsheet_update_info(
                            current_spreadsheet['updated_time'],
                            current_spreadsheet['id']
                        ))


# block Интервью {
@bot.message_handler(Filters.change_group)
async def new_index(event: BotEvent):
    await fsm.set_state(event=event, state=GROUP_INDEX, for_what=ForWhat.FOR_CHAT)
    return Strings.CHANGE_GROUP_MESSAGE


# } block Получение индекса {
@bot.message_handler(StateFilter(fsm=fsm, state=GROUP_INDEX, for_what=ForWhat.FOR_CHAT), )
async def new_index(event: BotEvent):
    received_message = event.object.object.message.text

    if "бот" in received_message:
        received_message = received_message[4:]

    if not received_message.isdigit():
        return Strings.INVALID_INPUT_MESSAGE
    await fsm.add_data(
        event=event,
        for_what=ForWhat.FOR_CHAT,
        state_data={"group_index": received_message},
    )
    user_data = await fsm.get_data(event=event, for_what=ForWhat.FOR_CHAT)

    await fsm.finish(event=event, for_what=ForWhat.FOR_CHAT)

    # }

    Database(event.object.object.message.peer_id).update_group_index(user_data['group_index'])

    return f"Ваша новая группа: {user_data['group_index']}"


# ... Дебаг ...
@bot.message_handler(bot.text_contains_filter("baba111"))
async def dev(event: SimpleBotEvent):
    cp = ClassProcessor(get_group_index(event))
    await event.answer(message=cp.getByDay(0))


# ... Расписание ...
@bot.message_handler(Filters.this_week)
async def timetable(event: SimpleBotEvent):
    await event.answer(message=Strings.DEFAULT_ANSWER_MESSAGE, keyboard=Keyboards.week().get_keyboard())


@bot.message_handler(Filters.next_week)
async def timetable(event: SimpleBotEvent):
    await event.answer(message=Strings.DEFAULT_ANSWER_MESSAGE, keyboard=Keyboards.week_next().get_keyboard())


@bot.message_handler(PayloadContainsFilter("show day"))
async def timetable(event: SimpleBotEvent):
    payload = event.payload
    cp = ClassProcessor(get_group_index(event))

    if payload['next week']:
        await event.answer(message=cp.getByDay(week_day_index=payload['day'], next_week=True))
    else:
        await event.answer(message=cp.getByDay(week_day_index=payload['day']))


# ... Навигация ...
@bot.message_handler(Filters.kill_keyboard)
async def navigation(event: SimpleBotEvent):
    await event.answer(message=Strings.DEFAULT_ANSWER_MESSAGE)


@bot.message_handler(Filters.main_menu)
async def navigation(event: SimpleBotEvent):
    await event.answer(message=Strings.DEFAULT_ANSWER_MESSAGE, keyboard=Keyboards.main().get_keyboard())


@bot.message_handler()
async def echo(event: SimpleBotEvent) -> str:
    return Strings.INVALID_COMMAND


print("started")
CLONES.run_all_bots()
