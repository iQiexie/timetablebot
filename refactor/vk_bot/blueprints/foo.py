from vkbottle.bot import Blueprint, Message

foo_bp = Blueprint()


@foo_bp.on.message(text="пока")
async def bye_handler(message: Message):
    await message.answer("Пока...")


@foo_bp.on.message(text="до<!>свидания<!>")
async def goodbye_handler(message: Message):
    await message.answer("Надеюсь, скоро увидимся!")
