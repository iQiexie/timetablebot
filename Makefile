format:
	black --line-length 100 .
migrations:
	alembic revision --autogenerate -m "$(m)"
migrate:
	alembic upgrade head