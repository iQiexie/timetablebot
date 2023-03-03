format:
	black --line-length 100 .
migrations:
	alembic revision --autogenerate -m "$(m)"
migrate:
	alembic upgrade head
make deploy:
	docker-compose -f prod.yml --env-file .env up --build