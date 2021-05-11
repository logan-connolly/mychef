.PHONY: build pull download start scrape lint tests clean

build:
	docker-compose build

pull:
	docker-compose pull

download:
	./scripts/download-models.sh

run: pull
	docker-compose up -d ui

scrape: run
	docker-compose run --rm scraper

lint:
	pre-commit run --all-files

tests:
	docker-compose pull api
	docker-compose up -d api
	docker-compose exec api pytest tests

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
