from vkbottle.bot import Blueprint
from vkbottle.bot import Message

from app.backend.handlers.chatgpt.handler import delete_context
from app.backend.handlers.chatgpt.handler import send_message
from app.backend.handlers.chatgpt.handler import start_chat
from app.backend.handlers.chatgpt.redis import ChatGptREDIS
from app.backend.handlers.users.schemes import UserSchema
from app.vk_bot.blueprints.chat_gpt.states import ChatGptStates
from app.vk_bot.blueprints.chat_gpt.strings import dummy_answer
from app.vk_bot.blueprints.chat_gpt.strings import hello_text
from app.vk_bot.bots import current_bot
from app.vk_bot.keyboards.chat_gpt import get_gpt_keyboard
from app.vk_bot.rules.contains_trigger import ContainsTriggerRule

blueprint = Blueprint()


@blueprint.on.message(ContainsTriggerRule(payload_triggers=["chatgpt"]))
async def start_chat_gpt(message: Message, user: UserSchema):
    redis = ChatGptREDIS()

    user_peer = await current_bot.api.users.get(message.from_id)
    name = user_peer[0].id, user_peer[0].first_name

    await message.answer(
        hello_text,
        keyboard=get_gpt_keyboard(state=ChatGptStates.WAITING_FOR_ANSWER),
    )
    result = await start_chat(
        vk_id=int(user.vk_id), redis=redis, conversation_opener=f"Привет! Меня зовут {name}"
    )

    answer = result or "Чем могу помочь?"

    await blueprint.state_dispenser.set(message.peer_id, ChatGptStates.CHATTING)
    await message.answer(answer, keyboard=get_gpt_keyboard(ChatGptStates.CHATTING))


@blueprint.on.message(ContainsTriggerRule(payload_triggers=["gpt stop"]))
async def stop_chat_gpt(message: Message, user: UserSchema):
    await message.answer(f"Чат остановлен", keyboard=get_gpt_keyboard(ChatGptStates.NOT_CHATTING))
    await blueprint.state_dispenser.delete(message.peer_id)


@blueprint.on.message(ContainsTriggerRule(payload_triggers=["gpt delete"]))
async def stop_chat_gpt(message: Message, user: UserSchema):
    await delete_context(vk_id=int(user.vk_id))
    await message.answer(f"Чат удалён", keyboard=get_gpt_keyboard(ChatGptStates.NOT_CHATTING))

    await blueprint.state_dispenser.set(message.peer_id, ChatGptStates.CHATTING)


@blueprint.on.message(ContainsTriggerRule(payload_triggers=["gpt_status"]))
async def stop_chat_gpt(message: Message, user: UserSchema):
    await message.answer(
        f"Эта кнопка ничего не делает. Она лишь показывает, в каком статусе сейчас "
        f"находится ChatGPT"
    )


@blueprint.on.message(state=ChatGptStates.CHATTING)
async def chat(message: Message, user: UserSchema):
    await message.answer(dummy_answer, keyboard=get_gpt_keyboard(ChatGptStates.WAITING_FOR_ANSWER))
    response = await send_message(vk_id=int(user.vk_id), message=message.text)
    await message.answer(response, keyboard=get_gpt_keyboard(ChatGptStates.CHATTING))
