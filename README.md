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

Сначала создаём файлики: `deploy/.env`, `deploy/.env.local` и прописываем там всё в соответствии с `deploy/.env.example`

### Первый раз:

1. Запускаем приложение `make deploy`
2. Обновляем пары вручную `docker exec -t -e ENV_FILE=deploy/.env -e ROUTINE=ACTUALIZE timetablebot-python python main.py`
3. Переходим по ссылке из логов и входим в свой гугл аккаунт
4. Копируем юрл из браузера, на которую нас перекинуло
5. Открываем новый терминал и запускаем команду `docker exec -t timetablebot-python curl "скопированный юрл"` (ЮРЛ ВСТАВЛЯЕМ ВНУТРИ КАВЫЧЕК!)
6. Переходим в первый терминал и убеждаемся, что парсинг выполнился


### Сдедующие запуски:

1. Запускаем приложение `make deploy`


## Contribute

Новые БД модели должны быть импортированы тут `app.backend.db.__init__.py`  (Для совместимости с алембиком)

Новые ВК мидлвари должны быть импортированы тут `app.vk_bot.middlewares.__init__.py`

Новые ВК блупринты должны быть импортированы тут `app.vk_bot.blueprints.__init__.py`

#### Команды

`make actualize` - Обновляем пары вручную (локально) 

`make run` - Запускаем локально

`make stop` - Останавливаем локально

#### Енвы

- `.env` - продовые переменные окружения
- `.env.local` - переменные окружения для разработки

## TODO:

- [ ] CI/CD
- [ ] Сделать так, чтобы сообщения от ChatGPT присылались как сообщение-ответ (с ссылкой на промпт)
- [ ] Нормальная рассылка новостей
- [ ] Пофиксить баг с ```2023-03-16 17:50:19.184 UTC [312] FATAL:  password authentication failed for user "postgres"
2023-03-16 17:50:19.184 UTC [312] DETAIL:  Password does not match for user "postgres".
        Connection matched pg_hba.conf line 99: "host all all all md5"``` при `make deploy` 