FROM python:3.10-bullseye
ENV PYTHONPATH /usr/app/
RUN apt-get update && apt-get install -y tzdata cron
RUN ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime && dpkg-reconfigure -f noninteractive tzdata


WORKDIR /usr/app/

COPY Pipfile.lock Pipfile ./
RUN pip install pipenv
RUN pipenv install --system

COPY . .
