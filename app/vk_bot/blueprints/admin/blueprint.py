from vkbottle.bot import Blueprint, Message
import multiprocessing as mp

from app.vk_bot.actualizer_utils import class_updater
from app.vk_bot.blueprints.admin.rules import UpdateClassesDbRule

admin_bp = Blueprint()


@admin_bp.on.message(UpdateClassesDbRule())
async def admin(message: Message):
    print('ok')
    await message.answer('added task')
    q = mp.Queue()
    p = mp.Process(target=class_updater)
    p.start()
    print(q.get())
    p.join()
    await message.answer('finished task')
