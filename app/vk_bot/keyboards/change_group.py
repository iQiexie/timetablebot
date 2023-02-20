from vkbottle import Keyboard
from vkbottle import KeyboardButtonColor
from vkbottle import Text

action = Text(
    label="Поменять группу",
    payload={"cmd": "change group"}
)

change_group_keyboard = Keyboard(inline=True)
change_group_keyboard.add(
    action=action,
    color=KeyboardButtonColor.PRIMARY,
)
