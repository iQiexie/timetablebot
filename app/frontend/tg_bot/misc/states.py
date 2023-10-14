from aiogram.dispatcher.fsm.state import State
from aiogram.dispatcher.fsm.state import StatesGroup


class FSMStates(StatesGroup):
    picking_group = State()
    pattern_input = State()
    pattern_search = State()
