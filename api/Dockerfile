FROM python:3.8-alpine3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

ARG POETRY="https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py"
ARG BUILD_DEPS="curl gcc g++ libc-dev musl-dev python3-dev postgresql-dev make"

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./poetry.lock* /app/

# Install poetry
RUN set -eux \
    && apk add --no-cache --virtual .build-deps $BUILD_DEPS \
    && apk add --no-cache libpq \
    && curl -sSL $POETRY | POETRY_HOME=/opt/poetry python \
    && cd /usr/local/bin \
    && ln -s /opt/poetry/bin/poetry \
    && poetry config virtualenvs.create false \
    && cd /app \
    && poetry install --no-root \
    && apk del .build-deps $BUILD_DEPS

COPY . .
