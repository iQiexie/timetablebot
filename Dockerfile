FROM python:3.10-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . .

RUN pip install pipenv
RUN pipenv install --system
