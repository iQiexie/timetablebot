from vkwave.bots import SimpleLongPollBot, SimpleBotEvent, BotEvent, ClonesBot, MiddlewareResult
from vkwave.bots.fsm import StateFilter

from Assets.Filters import CustomPayloadContainsFilter
from Assets.custom_fsm import FiniteStateMachine, ForWhat, State

from Assets import Keyboards, Filters, Strings
from Database import Database
from ClassProcessor import ClassProcessor
from SheetScraper import update_spreadsheet, delete_spreadsheet
from AiHandler import Ai_Handler
from Catchup import run_catchup

from threading import Timer
from datetime import datetime

from app.Assets.Strings import SERVER_OVERLOAD

MAIN_TOKEN = open('secret/tokenmain', 'r').read()  # домашка
MAIN_GROUP_ID = 198604544  # домашка

SCHEDULE_TOKEN = open('secret/token', 'r').read()  # расписание
SCHEDULE_GROUP_ID = 206763355  # расписание

MPSU_TOKEN = open('secret/tokenmpsu', 'r').read()  # расписание
MPSU_GROUP_ID = 152158632  # расписание

bot = SimpleLongPollBot(tokens=MAIN_TOKEN, group_id=MAIN_GROUP_ID)
new_bot = SimpleLongPollBot(tokens=SCHEDULE_TOKEN, group_id=SCHEDULE_GROUP_ID)
mpsu_bot = SimpleLongPollBot(tokens=MPSU_TOKEN, group_id=MPSU_GROUP_ID)

GROUP_INDEX = State("group_index")  # это нужно для fsm

fsm = FiniteStateMachine()
Ai = Ai_Handler()

CLONES = ClonesBot(
    bot,  # домашка
    new_bot,  # расписание
    mpsu_bot
)


def spreadsheet_updating_service():
    """Сохраняет копию гугл таблиц на драйв аккаунт. Вызывается каждый час"""

    if Strings.current_spreadsheet['id'] is not None:
        delete_spreadsheet(Strings.current_spreadsheet['id'])  # Удаляем старый документ, if it's in ram

    Strings.current_spreadsheet['id'] = update_spreadsheet()  # Создаём новый документ
    Strings.current_spreadsheet['updated_time'] = datetime.now().strftime('%H:%M')  # updating last doc creation time

    Timer(3600, spreadsheet_updating_service).start()


spreadsheet_updating_service()
run_catchup()


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
    db = Database(event.peer_id)
    if db.first_message:
        await event.answer(keyboard=Keyboards.main().get_keyboard(), message=Strings.GREETINGS)
    else:
        await event.answer(keyboard=Keyboards.main().get_keyboard(), message=Strings.DEFAULT_ANSWER_MESSAGE)


# ... Сегодняшние и Завтрашние пары ...
@bot.message_handler(Filters.today)
async def today(event: SimpleBotEvent):
    """ Отправка пар на сегодня """

    cp = ClassProcessor(get_group_index(event))
    if not cp.initialized:
        await event.answer(message=SERVER_OVERLOAD + f"\n\nReason: {cp.not_initialized_reason}")

    await event.answer(message=cp.get_today(), keyboard=Keyboards.main().get_keyboard())


@bot.message_handler(Filters.tomorrow)
async def today(event: SimpleBotEvent):
    """ Отправка пар на завтра """

    cp = ClassProcessor(get_group_index(event))
    if not cp.initialized:
        await event.answer(message=SERVER_OVERLOAD + f"\n\nReason: {cp.not_initialized_reason}")

    await event.answer(message=cp.get_tomorrow(), keyboard=Keyboards.main().get_keyboard())


# ... Настройки ...
@bot.message_handler(Filters.settings)
async def settings(event: SimpleBotEvent):
    """ Отправка клавиатуры настроек """

    await event.answer(message=Strings.Settings(get_group_index(event)),
                       keyboard=Keyboards.settings(event.peer_id).get_keyboard())


@bot.message_handler(Filters.last_update_time)
async def settings(event: SimpleBotEvent):
    """ Когда расписание обновлялось последний раз """

    await event.answer(message=Strings.Spreadsheet_update_info())


@bot.message_handler(bot.text_contains_filter("&a=public-api"))
async def settings(event: SimpleBotEvent):
    """ Обновление кредитов p-bot'a """

    new_creds = event.object.object.message.text
    Ai.update_creds(new_creds)
    await event.answer(message="New credits: " + new_creds)


@bot.message_handler(Filters.update_ai)
async def settings(event: SimpleBotEvent):
    """ Обновление ии """

    db = Database(event.peer_id)

    if db.get_ai() == 1:
        db.update_ai(0)
        action = "выключен"
    else:
        db.update_ai(1)
        action = "включён"

    await event.answer(message=Strings.AI_FRIEND + action, keyboard=Keyboards.settings(event.peer_id).get_keyboard())


# block Интервью {
@bot.message_handler(Filters.change_group)
async def new_index(event: BotEvent):
    await fsm.set_state(event=event, state=GROUP_INDEX, for_what=ForWhat.FOR_CHAT)
    return Strings.CHANGE_GROUP_MESSAGE


# } block Получение индекса {
@bot.message_handler(StateFilter(fsm=fsm, state=GROUP_INDEX, for_what=ForWhat.FOR_CHAT))
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
    update_spreadsheet()
    await event.answer(message="spreadsheet created")


@bot.message_handler(bot.text_contains_filter("catchup"))
async def dev(event: SimpleBotEvent):
    run_catchup()
    await event.answer(message="ertgergerger")


# ... Расписание ...
@bot.message_handler(Filters.this_week)
async def timetable(event: SimpleBotEvent):
    """ Отправка клавиатуры с текущей неделей """

    await event.answer(message=Strings.DEFAULT_ANSWER_MESSAGE, keyboard=Keyboards.week().get_keyboard())


@bot.message_handler(Filters.next_week)
async def timetable(event: SimpleBotEvent):
    """ Отправка клавиатуры со следующей неделей """

    await event.answer(message=Strings.DEFAULT_ANSWER_MESSAGE, keyboard=Keyboards.week_next().get_keyboard())


@bot.message_handler(CustomPayloadContainsFilter("show day"))
async def timetable(event: SimpleBotEvent):
    payload = event.payload
    cp = ClassProcessor(get_group_index(event))
    if not cp.initialized:
        await event.answer(message=SERVER_OVERLOAD + f"\n\nReason: {cp.not_initialized_reason}")

    if payload['next week']:
        await event.answer(message=cp.getByDay(week_day_index=payload['day'], next_week=True))
    else:
        await event.answer(message=cp.getByDay(week_day_index=payload['day']))


# ... Навигация ...
@bot.message_handler(Filters.kill_keyboard)
async def navigation(event: SimpleBotEvent):
    """ Отправка сообщения при нажатии на "Убрать клавиатуру" """

    await event.answer(message=Strings.DEFAULT_ANSWER_MESSAGE)


@bot.message_handler(Filters.main_menu)
async def navigation(event: SimpleBotEvent):
    """ Отправка клавиатуры с главным меню """

    await event.answer(message=Strings.DEFAULT_ANSWER_MESSAGE, keyboard=Keyboards.main().get_keyboard())


@bot.message_handler()
async def echo(event: SimpleBotEvent) -> str:

    db = Database(event.peer_id)

    if event.object.group_id == MPSU_GROUP_ID:
        return
        # return Strings.WRONG_COMMUNITY

    # если виртуальный собеседник включён
    if db.get_ai() == 1:
        return Ai.get_response(event.object.object.message.text, event.peer_id)
    else:
        return Strings.INVALID_COMMAND


print("started")
CLONES.run_all_bots()
