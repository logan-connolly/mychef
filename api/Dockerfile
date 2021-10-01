FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /tmp/requirements.txt
RUN apt-get update && apt-get install -y gcc curl \
    && python -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache -U pip setuptools wheel \
    && /opt/venv/bin/pip install --no-cache -r /tmp/requirements.txt \
    && apt-get purge -y gcc \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/list/*

COPY . .
EXPOSE 8000
CMD ["/start.sh"]
