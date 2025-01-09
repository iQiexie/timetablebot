# Код бота, которого я сделал для своего универа


## Deploy

Сначала создаём файлик `./timetable-infra/.env.prod` и прописываем там всё в соответствии с `./timetable-infra/.env.example`

### Первый раз:

1. Запускаем приложение `docker-compose -f timetable-infra/prod.docker-compose.yml up --build`
2. Обновляем пары вручную `docker exec -t -e URL=/v1/classes -e METHOD=PATCH timetable-backend /usr/local/bin/python /usr/app/cron.py`
3. Переходим по ссылке из логов и входим в свой гугл аккаунт
4. Копируем юрл из браузера, на которую нас перекинуло
5. Открываем новый терминал и запускаем команду `docker exec -t timetable-backend curl "скопированный юрл"` (ЮРЛ ВСТАВЛЯЕМ ВНУТРИ КАВЫЧЕК!)
6. Переходим в первый терминал и убеждаемся, что парсинг выполнился


### Сдедующие запуски:

1. Запускаем приложение `make deploy`


#### Енвы

- `.env` - переменные окружения для разработки
- `./timetable-infra/.env.prod` - продовые переменные окружения
