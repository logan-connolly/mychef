.PHONY: install build publish update

image = lvconnolly/mychef_api:dev

install:
	poetry install

update:
	poetry update

build: install
	poetry export --dev --without-hashes -o requirements.txt
	docker build -t ${image} .

publish: build
	docker push ${image}
