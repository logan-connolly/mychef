FROM python:3.9-slim-buster

ARG BUILD_DEPS="curl gcc musl-dev python3-dev"
WORKDIR /app
COPY requirements/production.txt /tmp/requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH="/opt/venv/bin:$PATH"

RUN apt-get update && apt-get install --no-install-recommends -y ${BUILD_DEPS} \
    && python -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache -U pip setuptools wheel \
    && /opt/venv/bin/pip install --no-cache -r /tmp/requirements.txt \
    && apt-get remove --purge -y ${BUILD_DEPS} \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/list/*

COPY . .

ENTRYPOINT ["scrapy"]
