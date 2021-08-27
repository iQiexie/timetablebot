from vkwave.bots import SimpleLongPollBot, SimpleBotEvent, PayloadFilter
from Assets import Keyboards

main_id = open('Assets/token', 'r').read()
main_group_id = 198604544

bot = SimpleLongPollBot(tokens=main_id, group_id=main_group_id)

DEFAULT_ANSWER = 'Ok'


@bot.message_handler(bot.text_contains_filter("1"))
async def echo(event: SimpleBotEvent):
    await event.answer(keyboard=Keyboards.main().get_keyboard(), message="лул")


@bot.message_handler(PayloadFilter({"command": "kill keyboard"}))
async def all(event: bot.SimpleBotEvent):
    await event.answer(message=DEFAULT_ANSWER)


print("started")
bot.run_forever()
