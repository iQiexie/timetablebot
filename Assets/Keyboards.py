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
        text="Расписание на неделю", color=ButtonColor.SECONDARY, payload={"command": "this week"}
    )

    main.add_text_button(
        text="Расписание на след. неделю", color=ButtonColor.SECONDARY, payload={"command": "next week"}
    )

    main.add_row()

    main.add_text_button(
        text="Убрать клавиатуру", color=ButtonColor.NEGATIVE, payload={"command": "kill keyboard"}
    )

    return main
