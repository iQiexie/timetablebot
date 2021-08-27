from vkwave.bots import Keyboard, ButtonColor


def main() -> Keyboard:
    kb = Keyboard(one_time=False) # TODO поменять на True

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
                                                              "day": "monday",
                                                              "next week": False})
    kb.add_text_button(
        text="Вторник", color=ButtonColor.SECONDARY, payload={"command": "show day",
                                                              "day": "tuesday",
                                                              "next week": False})

    kb.add_row()

    kb.add_text_button(
        text="Среда", color=ButtonColor.SECONDARY, payload={"command": "show day",
                                                            "day": "wednesday",
                                                            "next week": False})
    kb.add_text_button(
        text="Четверг", color=ButtonColor.SECONDARY, payload={"command": "show day",
                                                              "day": "thursday",
                                                              "next week": False})

    kb.add_row()

    kb.add_text_button(
        text="Пятница", color=ButtonColor.SECONDARY, payload={"command": "show day",
                                                              "day": "friday",
                                                              "next week": False})
    kb.add_text_button(
        text="Суббота", color=ButtonColor.SECONDARY, payload={"command": "show day",
                                                              "day": "saturday",
                                                              "next week": False})

    kb.add_row()

    kb.add_text_button(
        text="В меню", color=ButtonColor.NEGATIVE, payload={"command": "main menu"}
    )

    return kb


def week_next() -> Keyboard:
    kb = Keyboard(one_time=False)

    kb.add_text_button(
        text="Понедельник", color=ButtonColor.SECONDARY, payload={"command": "show day",
                                                                  "day": "monday",
                                                                  "next week": True})
    kb.add_text_button(
        text="Вторник", color=ButtonColor.SECONDARY, payload={"command": "show day",
                                                              "day": "tuesday",
                                                              "next week": True})

    kb.add_row()

    kb.add_text_button(
        text="Среда", color=ButtonColor.SECONDARY, payload={"command": "show day",
                                                            "day": "wednesday",
                                                            "next week": True})
    kb.add_text_button(
        text="Четверг", color=ButtonColor.SECONDARY, payload={"command": "show day",
                                                              "day": "thursday",
                                                              "next week": True})

    kb.add_row()

    kb.add_text_button(
        text="Пятница", color=ButtonColor.SECONDARY, payload={"command": "show day",
                                                              "day": "friday",
                                                              "next week": True})
    kb.add_text_button(
        text="Суббота", color=ButtonColor.SECONDARY, payload={"command": "show day",
                                                              "day": "saturday",
                                                              "next week": True})

    kb.add_row()

    kb.add_text_button(
        text="В меню", color=ButtonColor.NEGATIVE, payload={"command": "main menu"}
    )

    return kb
