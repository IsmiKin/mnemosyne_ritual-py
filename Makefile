PYTHONPATH=$(CURDIR)

.PHONY: all

test:
	coverage run --source=matcher/,matcher/score,matcher/data --omit=*/test* -m pytest --strict
	coverage report -m

install:
	pipenv install

build:
	docker-compose build

clean-docker-run:
	docker rm $(docker ps -aq -f status=exited)

clean-build:
	docker rm $(docker ps -aq -f status=exited)
	docker rmi mnemosyne*

up-dev: build
	docker-compose down
	docker-compose up --force-recreate -d

attach-dev: up-dev
	docker exec -it mnemosyne_ritual-py-mnemosyne-1 bash

clean:
	@echo "To be defined"