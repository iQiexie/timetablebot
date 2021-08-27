from vkwave.bots import Keyboard, ButtonColor


def main() -> Keyboard:
    main = Keyboard(one_time=True)
    main.add_text_button(
        text="Сегодняшние пары", color=ButtonColor.PRIMARY, payload={"command": "today"}
    )
    main.add_text_button(
        text="Завтрашние пары", color=ButtonColor.PRIMARY, payload={"command": "tomorrow"}
    )

    main.add_row()

    main.add_text_button(
        text="Эта неделя", color=ButtonColor.SECONDARY, payload={"command": "this week"}
    )

    main.add_text_button(
        text="Настройки", color=ButtonColor.SECONDARY, payload={"command": "settings"}
    )

    main.add_text_button(
        text="Следующая неделя", color=ButtonColor.SECONDARY, payload={"command": "next week"}
    )

    main.add_row()

    main.add_text_button(
        text="Убрать клавиатуру", color=ButtonColor.NEGATIVE, payload={"command": "kill keyboard"}
    )

    return main


def settings() -> Keyboard:
    main = Keyboard(one_time=False)
    main.add_text_button(
        text="Поменять группу", color=ButtonColor.PRIMARY, payload={"command": "change group"}
    )
    main.add_text_button(
        text="Наша группа", color=ButtonColor.PRIMARY, payload={"command": "settings"}
    )
    main.add_row()

    main.add_text_button(
        text="В меню", color=ButtonColor.NEGATIVE, payload={"command": "main menu"}
    )

    return main
