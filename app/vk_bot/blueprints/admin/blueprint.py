from vkbottle.bot import Blueprint, Message
import multiprocessing as mp

from app.vk_bot.actualizer_utils import class_updater
from app.vk_bot.blueprints.admin.rules import UpdateClassesDbRule

admin_bp = Blueprint()


@admin_bp.on.message(UpdateClassesDbRule())
async def today_classes_filter(message: Message):
    q = mp.Queue()
    p = mp.Process(target=class_updater)
    p.start()
    print(q.get())
    p.join()
    await message.answer('added task')
