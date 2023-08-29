ENV_FILE_LOCAL = ./deploy/.env.local
ENV_FILE_PROD = ./deploy/.env

COMPOSE_FILE_LOCAL = ./deploy/local.yml
COMPOSE_FILE_PROD = ./deploy/prod.yml

POSTGRES_CONTAINER = timetable-postgres
REDIS_CONTAINER = timetable-redis

.PHONY: format migrations migrate deploy run stop actualize

format:
	black --line-length 100 .
migrations:
	ENV_FILE=$(ENV_FILE_LOCAL) alembic revision --autogenerate -m "$(m)"
migrate:
	ENV_FILE=$(ENV_FILE_LOCAL) alembic upgrade head
deploy:
	docker-compose -f $(COMPOSE_FILE_PROD) --env-file $(ENV_FILE_PROD) up --build -d
logs:
	docker logs timetablebot-python -f
run:
	@POSTGRES_RUNNING=$$(docker ps --filter "name=$${POSTGRES_CONTAINER}" --format "{{.Names}}" | grep -w "$${POSTGRES_CONTAINER}") ;\
	REDIS_RUNNING=$$(docker ps --filter "name=$${REDIS_CONTAINER}" --format "{{.Names}}" | grep -w "$${REDIS_CONTAINER}") ;\
	if [ -z "$${POSTGRES_RUNNING}" ] || [ -z "$${REDIS_RUNNING}" ]; then \
	    docker-compose -f $(COMPOSE_FILE_LOCAL) --env-file $(ENV_FILE_LOCAL) up -d ;\
	    ENV_FILE=$(ENV_FILE_LOCAL) python main.py ;\
	else \
	    ENV_FILE=$(ENV_FILE_LOCAL) python main.py ;\
	fi
stop:
	docker-compose -f $(COMPOSE_FILE_LOCAL) down
actualize:
	docker exec timetablebot-python ROUTINE=ACTUALIZE ENV_FILE=$(ENV_FILE_LOCAL) python main.py
