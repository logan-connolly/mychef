FROM tiangolo/uvicorn-gunicorn:python3.8-slim

ARG POETRY="https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py"
ARG BUILD_DEPS="curl"
WORKDIR /app
COPY ./pyproject.toml ./poetry.lock* /app/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

RUN set -eux \
    && apt-get update && apt-get install --no-install-recommends -y ${BUILD_DEPS} \
    && curl -sSL $POETRY | POETRY_HOME=/opt/poetry python \
    && cd /usr/local/bin \
    && ln -s /opt/poetry/bin/poetry \
    && poetry config virtualenvs.create false \
    && cd /app \
    && poetry install --no-root \
    && apt-get remove --purge -y ${BUILD_DEPS} \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/list/*

COPY . .
