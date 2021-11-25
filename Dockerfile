FROM python:3.9.6

ENV PYTHONPATH=/webscraper \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.6

WORKDIR /webscraper
COPY . /webscraper
WORKDIR /webscraper/app

RUN rm -rf /usr/local/lib/python3.9/site-packages
RUN cp -r venv/Lib/site-packages /usr/local/lib/python3.9/

CMD ["python3", "-u", "main.py"]