from vkbottle import Keyboard, Text, KeyboardButtonColor


def compose_feedback_keyboard(context: dict):
    feedback_keyboard = Keyboard(inline=True)
    feedback_keyboard.add(
        Text("👍 Правильно", payload={"cmd": "upvote", **context}),
        color=KeyboardButtonColor.POSITIVE,
    )
    feedback_keyboard.add(
        Text("👎 Неправильно", payload={"cmd": "downvote", **context}),
        color=KeyboardButtonColor.NEGATIVE,
    )
    return feedback_keyboard
