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
RUN pip install --no-cache-dir -r requirements.txt


ENTRYPOINT ["gunicorn", "app:api" "-c", "mychef_scraper/config/gunicorn_conf.py", "--reload"]

