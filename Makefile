.PHONY: build pull download start scrape clean

build:
	docker-compose build

pull:
	docker-compose pull

download:
	./scripts/download-models.sh

run: pull
	docker-compose up -d ui

scrape:
	docker-compose run scraper

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
