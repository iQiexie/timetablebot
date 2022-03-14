import logging
from datetime import datetime
from config import settings

logging.basicConfig(level=settings.logging_level)


def get_logger(name: str, level=None):
    logger = logging.getLogger(f" {name} ")
    logger.setLevel(level=level or settings.logging_level)

    return logger


def list_contains_str(message: str, triggers: list[str]) -> bool:
    for trigger in triggers:
        if trigger in message.lower():
            return True


async def safe_pop(array: list, index: int):
    if index >= len(array):
        return array
    else:
        res = array.pop(index)
        if res == "":
            return None
        return res


def safe_get(array: list, index: int):
    if array is None:
        return None
    if index >= len(array):
        return None
    else:
        return array[index]


async def safe_get_dict(array: dict, key: str):
    if type(array) == dict:
        return array.get(key)
    else:
        return None


def columns_to_pydantic(result, model):
    dict_ = {}
    for key in result.__mapper__.c.keys():
        dict_[key] = getattr(result, key)

    return model(**dict_)


def smart_list_merge(first_list: list[str], second_list: list[str]) -> list[str]:
    ultimate_list = []
    for string in first_list:
        for _string in second_list:
            smart_string = f'{string} {_string}'
            super_smart_string = f'{_string} {string}'

            ultimate_list.append(smart_string)
            ultimate_list.append(super_smart_string)

    return ultimate_list


def is_week_above(week: int) -> bool:
    return week % 2 != 0
