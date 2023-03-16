FROM python:3.10-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y tzdata cron
RUN ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime && dpkg-reconfigure -f noninteractive tzdata


WORKDIR /app
COPY . .

RUN pip install pipenv
RUN pipenv install --system

RUN echo "$(cat deploy/crontab)" | crontab -