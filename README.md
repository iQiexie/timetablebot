# Бот-расписание для моего университета

https://vk.com/mpsu_schedule

## Стек

- Backend: fastapi + postgres + sqlalchemy
- Frontend: vkbottles + aiogram


## Deploy

Сначала создаём файлики: `deploy/.env`, `deploy/.env.local` и прописываем там всё в соответствии с `deploy/.env.example`

### Первый раз:

1. Запускаем приложение `docker-compose -f timetable-infra/prod.docker-compose.yml up --build`
2. Обновляем пары вручную `docker exec -t -e URL=/v1/classes -e METHOD=PATCH timetable-backend /usr/local/bin/python /usr/app/cron.py`
3. Переходим по ссылке из логов и входим в свой гугл аккаунт
4. Копируем юрл из браузера, на которую нас перекинуло
5. Открываем новый терминал и запускаем команду `docker exec -t timetable-backend curl "скопированный юрл"` (ЮРЛ ВСТАВЛЯЕМ ВНУТРИ КАВЫЧЕК!)
6. Переходим в первый терминал и убеждаемся, что парсинг выполнился


### Сдедующие запуски:

1. Запускаем приложение `make deploy`


## Contribute

- Устанавливаем пре-коммит хуки `pre-commit install`
- Новые БД модели должны быть импортированы тут `app.backend.db.base.py`  (Для совместимости с алембиком)
- Новые ВК мидлвари должны быть импортированы тут `app.frontend.vk_bot.middlewares.__init__.py`
- Новые ВК блупринты должны быть импортированы тут `app.frontend.vk_bot.blueprints.__init__.py`

#### Енвы

- `.env` - переменные окружения для разработки
- `./timetable-infra/.env.prod` - продовые переменные окружения


## TODO:

- [ ] добавить в статистику просмотр uptime'a
