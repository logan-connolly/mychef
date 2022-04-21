FROM python:3.9-slim-buster as prod

COPY requirements/production.txt /tmp/requirements.txt
RUN apt-get update && apt-get install -y gcc curl \
    && python -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache -U pip setuptools wheel \
    && /opt/venv/bin/pip install --no-cache -r /tmp/requirements.txt \
    && apt-get purge -y gcc \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/list/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/opt/mychef \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /opt/mychef
COPY . .
EXPOSE 8000
CMD ["./start.sh"]

FROM prod as dev
COPY requirements/development.txt /tmp/requirements-dev.txt
RUN /opt/venv/bin/pip install --no-cache -r /tmp/requirements-dev.txt
