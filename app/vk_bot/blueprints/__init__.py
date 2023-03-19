from app.vk_bot.blueprints.statistics import blueprint as admin_blueprint
from app.vk_bot.blueprints.initial import blueprint as initial_blueprint
from app.vk_bot.blueprints.kill_keyboard import blueprint as kill_keyboard_blueprint
from app.vk_bot.blueprints.search_classes.blueprint import blueprint as classes_blueprint
from app.vk_bot.blueprints.feedback import blueprint as feedback_blueprint
from app.vk_bot.blueprints.settings.blueprint import blueprint as settings_blueprint
from app.vk_bot.blueprints.statistics import blueprint as statistics_blueprint
from app.vk_bot.blueprints.chat_gpt.blueprint import blueprint as gpt_blueprint

blueprints = [
    admin_blueprint,
    initial_blueprint,
    kill_keyboard_blueprint,
    classes_blueprint,
    feedback_blueprint,
    settings_blueprint,
    statistics_blueprint,
    gpt_blueprint,
]
