from vkbottle.bot import Blueprint, Message

from refactor.vk_bot.misc.states import PickingState

general_bp = Blueprint()


@general_bp.on.message(HelloRule())
async def bye_handler(message: Message):
    answer_message = (
        'Привет! Для начала работы с ботом тебе нужно написать "Старт" или "Начать", '
        'а потом тебе нужно поменять свою группу через настройки.'
        '\n\nСписок команд:'
        '\n vk.com/@mpsu_schedule-vse-komandy-bota'
    )
    await message.answer(answer_message)


@general_bp.on.message(text=".+?text.+?")
async def bye_handler(message: Message):
    state = PickingState.PICKING_GROUP
    error_message = 'Принимаются ответы только в цифрах от 100 до 500'

    await general_bp.state_dispenser.set(message.peer_id, state, error=error_message)
    await message.answer('Напиши номер своей группы')


@general_bp.on.message(state=PickingState.PICKING_GROUP)
async def bye_handler(message: Message):
    if message.text.isdigit():
        await message.answer(f"ты выбрал группу. Она: {message.text}")
        await general_bp.state_dispenser.delete(message.peer_id)
    else:
        await message.answer(f"Напиши цифру сука, а не {message.text}")
