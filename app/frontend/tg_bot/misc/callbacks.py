from enum import Enum
from typing import Optional

from aiogram.dispatcher.filters.callback_data import CallbackData


class Callback(CallbackData, prefix="t"):
    action: str
    data: Optional[str]


class CallbackActions(str, Enum):
    downvote = "downvote"
    upvote = "upvote"
    today = "today"
    tomorrow = "tomorrow"
    by_day = "by_day"
    pattern_search = "pattern_search"
    stop_pattern_search = "stop_pattern_search"
    sweek = "sweek"
    detailed = "detailed"
    searching_status = "searching_status"
    settings = "settings"
    suicide = "suicide"
    change_group = "change_group"
    uptime = "uptime"
    statistics = "statistics"
    menu = "menu"
    gpt = "gpt"
