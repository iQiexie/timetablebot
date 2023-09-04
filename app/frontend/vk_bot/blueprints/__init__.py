from app.frontend.vk_bot.blueprints.classes.feedback import blueprint as feedback_blueprint
from app.frontend.vk_bot.blueprints.classes.search_classes import blueprint as classes_blueprint
from app.frontend.vk_bot.blueprints.menu.initial import blueprint as initial_blueprint
from app.frontend.vk_bot.blueprints.menu.kill_keyboard import blueprint as kill_keyboard_blueprint
from app.frontend.vk_bot.blueprints.settings.settings_menu import blueprint as settings_blueprint

blueprints = [
    initial_blueprint,
    kill_keyboard_blueprint,
    classes_blueprint,
    feedback_blueprint,
    settings_blueprint,
]
