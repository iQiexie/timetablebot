from vkwave.bots import Keyboard, ButtonColor


def main() -> Keyboard:
    kb = Keyboard(one_time=True)

    kb.add_text_button(
        text="Сегодняшние пары", color=ButtonColor.PRIMARY, payload={"command": "today"}
    )
    kb.add_text_button(
        text="Завтрашние пары", color=ButtonColor.PRIMARY, payload={"command": "tomorrow"}
    )

    kb.add_row()

    kb.add_text_button(
        text="Эта неделя", color=ButtonColor.SECONDARY, payload={"command": "this week"}
    )

    kb.add_text_button(
        text="Настройки", color=ButtonColor.SECONDARY, payload={"command": "settings"}
    )

    kb.add_text_button(
        text="Следующая неделя", color=ButtonColor.SECONDARY, payload={"command": "next week"}
    )

    kb.add_row()

    kb.add_text_button(
        text="Убрать клавиатуру", color=ButtonColor.NEGATIVE, payload={"command": "kill keyboard"}
    )

    return kb


def settings() -> Keyboard:
    kb = Keyboard(one_time=False)

    kb.add_text_button(
        text="Поменять группу", color=ButtonColor.PRIMARY, payload={"command": "change group"}
    )
    kb.add_text_button(
        text="Наша группа", color=ButtonColor.PRIMARY, payload={"command": "settings"}
    )
    kb.add_row()

    kb.add_text_button(
        text="В меню", color=ButtonColor.NEGATIVE, payload={"command": "main menu"}
    )

    return kb


def week() -> Keyboard:
    kb = Keyboard(one_time=False)

    kb.add_text_button(
        text="Понедельник", color=ButtonColor.SECONDARY, payload={"command": "show day",
                                                                  "day": 0,
                                                                  "next week": False})
    kb.add_text_button(
        text="Вторник", color=ButtonColor.SECONDARY, payload={"command": "show day",
                                                              "day": 1,
                                                              "next week": False})

    kb.add_row()

    kb.add_text_button(
        text="Среда", color=ButtonColor.SECONDARY, payload={"command": "show day",
                                                            "day": 2,
                                                            "next week": False})
    kb.add_text_button(
        text="Четверг", color=ButtonColor.SECONDARY, payload={"command": "show day",
                                                              "day": 3,
                                                              "next week": False})

    kb.add_row()

    kb.add_text_button(
        text="Пятница", color=ButtonColor.SECONDARY, payload={"command": "show day",
                                                              "day": 4,
                                                              "next week": False})
    kb.add_text_button(
        text="Суббота", color=ButtonColor.SECONDARY, payload={"command": "show day",
                                                              "day": 5,
                                                              "next week": False})

    kb.add_row()

    kb.add_text_button(
        text="В меню (эта неделя)", color=ButtonColor.NEGATIVE, payload={"command": "main menu"}
    )

    return kb


def week_next() -> Keyboard:
    kb = Keyboard(one_time=False)

    kb.add_text_button(
        text="Понедельник", color=ButtonColor.SECONDARY, payload={"command": "show day",
                                                                  "day": 0,
                                                                  "next week": True})
    kb.add_text_button(
        text="Вторник", color=ButtonColor.SECONDARY, payload={"command": "show day",
                                                              "day": 1,
                                                              "next week": True})

    kb.add_row()

    kb.add_text_button(
        text="Среда", color=ButtonColor.SECONDARY, payload={"command": "show day",
                                                            "day": 2,
                                                            "next week": True})
    kb.add_text_button(
        text="Четверг", color=ButtonColor.SECONDARY, payload={"command": "show day",
                                                              "day": 3,
                                                              "next week": True})

    kb.add_row()

    kb.add_text_button(
        text="Пятница", color=ButtonColor.SECONDARY, payload={"command": "show day",
                                                              "day": 4,
                                                              "next week": True})
    kb.add_text_button(
        text="Суббота", color=ButtonColor.SECONDARY, payload={"command": "show day",
                                                              "day": 5,
                                                              "next week": True})

    kb.add_row()

    kb.add_text_button(
        text="В меню (след. неделя)", color=ButtonColor.NEGATIVE, payload={"command": "main menu"}
    )

    return kb
