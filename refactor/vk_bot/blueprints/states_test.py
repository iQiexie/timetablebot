from vkbottle.bot import Blueprint, Message

from refactor.vk_bot.states import PickingState

state_test = Blueprint()


@state_test.on.message(text="выбрать группу")
async def bye_handler(message: Message):
    state = PickingState.PICKING_GROUP
    error_message = 'Принимаются ответы только в цифрах от 100 до 500'

    await state_test.state_dispenser.set(message.peer_id, state, error=error_message)
    await message.answer('Напиши номер своей группы')


@state_test.on.message(state=PickingState.PICKING_GROUP)
async def bye_handler(message: Message):
    if message.text.isdigit():
        await message.answer(f"ты выбрал группу. Она: {message.text}")
        await state_test.state_dispenser.delete(message.peer_id)
    else:
        await message.answer(f"Напиши цифру сука, а не {message.text}")
