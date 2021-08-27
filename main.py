from vkwave.bots import SimpleLongPollBot, SimpleBotEvent, PayloadFilter, BotEvent
from vkwave.bots.fsm import FiniteStateMachine, StateFilter, ForWhat, State, ANY_STATE
from Assets import Keyboards
from Database import Database

main_id = open('secret/token', 'r').read()
main_group_id = 198604544

bot = SimpleLongPollBot(tokens=main_id, group_id=main_group_id)
fsm = FiniteStateMachine()

group_index = State("group_index")

DEFAULT_ANSWER = 'Ok'


# ... Cоздание бд для беседы, инициализация ...
@bot.message_handler(bot.text_contains_filter("старт"))
async def start(event: SimpleBotEvent):
    Database(event.peer_id)
    await event.answer(keyboard=Keyboards.main().get_keyboard(), message=DEFAULT_ANSWER)


# ... Настройки ...
@bot.message_handler(PayloadFilter({"command": "settings"}))
async def settings(event: bot.SimpleBotEvent):
    text = "Ваша группа: " + str(Database(event.peer_id).get_group_index())
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


@bot.message_handler(bot.text_contains_filter("qwe"))
async def dev(event: SimpleBotEvent):
    from SheetScraper import SheetScraper

    ss = SheetScraper(218)
    text = ss.read_column()

    print(text)
    await event.answer(message=text)


# ... Навигация ...
@bot.message_handler(PayloadFilter({"command": "kill keyboard"}))
async def navigation(event: bot.SimpleBotEvent):
    await event.answer(message=DEFAULT_ANSWER)


@bot.message_handler(PayloadFilter({"command": "main menu"}))
async def navigation(event: bot.SimpleBotEvent):
    await event.answer(message=DEFAULT_ANSWER, keyboard=Keyboards.main().get_keyboard())


print("started")
bot.run_forever()
