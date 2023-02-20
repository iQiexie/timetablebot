# Бот-расписание для моего университета

https://vk.com/mpsu_schedule

## Стек

- Data validation: pydantic
- Database: postgres
- Database ORM: sqlalchemy
- Migrations: alembic
- Cache: redis
- Cache framework: aioredis
- VK framework: vkbottle


## Deploy

Сначала создаём файлики: `.env`, `.env.routine` и прописываем там всё в соответствии с `.env.example`

Главное отличие `.env` от `.env.routine` в том, что в `.env.routine` - IP бд (localhost), а в `.env` - названия контейнеров (timetable-postgres) 

### Первый раз:

##### Инициализируем приложение

1. Запускаем приложуху `docker-compose --env-file ./.env up --build`
2. Ждём 3-4 секунды и накатываем миграции `docker exec -t timetablebot-python alembic upgrade head`

##### Настраиваем гугл аккаунт

1. Обновляем пары вручную `docker exec -t -e ENV_LOC=.env.routine -e ROUTINE=ACTUALIZE timetablebot-python python main.py`
2. Переходим по ссылке из логов и входим в свой гугл аккаунт
3. Копируем юрл из браузера, на которую нас перекинуло
4. Открываем новый терминал и запускаем команду `docker exec -t timetablebot-python curl "скопированный юрл"` (ЮРЛ ВСТАВЛЯЕМ ВНУТРИ КАВЫЧЕК!)
5. Переходим в первый терминал и убеждаемся, что парсинг выполнился

##### Настраиваем рутины

1. Запускаем команду `(crontab -l 2>/dev/null; echo "$(cat crontab)") | crontab -`


### Сдедующие запуски:

1. Запускаем приложуху `docker-compose --env-file ./.env up --build`
2. Ждём 3-4 секунды и накатываем миграции `docker exec -t timetablebot-python alembic upgrade head`
3. Запускаем команду `(crontab -l 2>/dev/null; echo "$(cat crontab)") | crontab -`


## Contribute

Новые БД модели должны быть импортированы тут `app.backend.db.__init__.py`  (Для совместимости с алембиком)

Новые ВК мидлвари должны быть импортированы тут `app.vk_bot.middlewares.__init__.py`

Новые ВК блупринты должны быть импортированы тут `app.vk_bot.blueprints.__init__.py`

Новые ВК клавиатуры должны быть импортированы тут `app.vk_bot.keyboards.__init.py`


- `.env` - production envs
- `.env.local` - local envs for development
- `.env.routine` - envs for cron on production server
