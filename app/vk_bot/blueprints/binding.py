from app.vk_bot.blueprints.admin.blueprint import admin_bp
from app.vk_bot.blueprints.classes.blueprint import classes_bp
from app.vk_bot.blueprints.settings.blueprint import settings_bp
from app.vk_bot.blueprints.general.blueprint import general_bp

blueprints = [general_bp, classes_bp, settings_bp, admin_bp]
