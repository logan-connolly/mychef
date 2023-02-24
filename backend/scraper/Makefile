.DEFAULT_GOAL=help

bootstrap: # Install dependencies
	pip install -r ./requirements/requirements.txt
	pip install -r ./requirements/dev-requirements.txt

debug: # Launch crawler in debug mode locally
	python -u -m debugpy --listen localhost:5678 --wait-for-client -m scrapy crawl full_helping

run: # Launch crawler locally
	scrapy crawl full_helping

lock: # Export dependency requirements files
	pip-compile -o ./requirements/requirements.txt ./requirements/requirements.in

clean: # Clean up cache files
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete

help: # Show this help
	@egrep -h '\s#\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
