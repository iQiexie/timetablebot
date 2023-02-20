New models are imported here `app.backend.db.__init__.py`  (For alembic detection)

New vk_bot middlewares are imported here `app.vk_bot.middlewares.__init__.py`

New vk_bot blueprints are imported here `app.vk_bot.blueprints.__init__.py`

New vk_bot keyboards are imported here `app.vk_bot.keyboards.__init.py`

.env - production envs
.env.local - local envs for development
.env.routine - envs for cron on production server


run actualize command: `ENV_LOC=.env.routine ROUTINE=ACTUALIZE python main.py`