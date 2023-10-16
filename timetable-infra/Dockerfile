FROM python:3.10-bullseye
ENV PYTHONPATH /usr/app/
RUN apt-get update && apt-get install -y tzdata cron
RUN ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

WORKDIR /usr/app/

RUN pip install pipenv
COPY Pipfile.lock Pipfile ./
RUN pipenv install --system

COPY . .
# возможно из-за этого будет гонка кронтабов среди всех инстансов (бека, телеги и вк)
RUN echo "$(cat timetable-infra/crontab)" | crontab -
