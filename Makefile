.DEFAULT_GOAL=help

assets: # Build frontend assets
	cd frontend && yarn build && yarn generate

build: # Build docker images locally
	docker-compose build

pull: # Pull required docker images
	docker-compose pull

push: # Push docker images to registry
	docker-compose push

download: # Download pretrained models
	./scripts/download-models.sh

run: # Start application containers
	docker-compose up -d proxy

scrape: # Run web scraper
	docker-compose run --rm scraper

lint: # Check and format via pre-commit
	pre-commit run --all-files

tests: # Launch services and test
	docker-compose pull api
	docker-compose up -d api
	docker-compose exec api pytest tests

clean: # Clean up cache files
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete

help: # Show this help
	@egrep -h '\s#\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
