## Стек

- Language: python
- Data validator: pydantic
- Database: postgres
- Database ORM: sqlalchemy
- Migration tool: alembic
- Cache database: redis
- Cache database framework: aioredis
- Вконтакте framework: vkbottle

## Деплой

- `docker network create timetableNetwork`
- `docker-compose up --build`
- Ctrl+c
- `docker network connect timetableNetwork timetablebot`
- `docker network connect timetableNetwork dabatabse`
- `docker network connect timetableNetwork redis`

- Копируем ip `docker network inspect -f '{{range.IPAM.Config}}{{.Gateway}}{{end}}' timetableNetwork`
- Вставляем в .env: `DB_HOST=скопированный айпи`; `REDIS_HOST=скопированный айпи`
- `docker-compose up --build`

Для первого запуска нужно выполнить следующие действия:
- Написать боту `обнови пары`
- Перейти по ссылке, которая появилась в терминале (скопировать её полностью)
- Авторизоваться через гугл аккаунт
- Скопировать самую последнюю ссылку, которая начинается с localhost
- Выполнить команду `docker exec timetablebot curl "скопированная ссылка"`
- Повторить всё то же самое для драйв сервиса

### Важно!!! Для запуска из пайчарма, в хосте надо обратно поменять на localhost, а то не будет подключаться