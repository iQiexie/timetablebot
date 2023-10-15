format:
	black --line-length 100 .
run:
	docker-compose -f timetable-infra/prod.docker-compose.yml up --build
stop:
	docker-compose -f timetable-infra/prod.docker-compose.yml down
