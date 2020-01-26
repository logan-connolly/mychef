FROM pypy:3-7-slim


WORKDIR /usr/src/app

# Install apt dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libffi-dev \
    libssl-dev \
    libpq-dev \
&& rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pypy3 -m venv /venv \
    && . /venv/bin/activate \
    && pip install -U pip setuptools \
    && pip install --no-cache-dir -r requirements.txt


COPY . .


CMD [ "sh", "entrypoint.sh" ]