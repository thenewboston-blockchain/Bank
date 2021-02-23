env_vars=. local/local.sh

.PHONY: build
build:
	docker build .

.PHONY: install
install:
	poetry install

.PHONY: test
test:
	poetry run pytest -v -n auto

.PHONY: test-dockerized
test-dockerized:
	docker-compose build bank  # to force rebuild the image for new changes
	docker-compose run bank pytest -v -n auto

.PHONY: lint
lint:
	# TODO(dmu) MEDIUM: Consider namespacing everything under single package
	poetry run flake8 thenewboston_bank tests config

.PHONY: migrate
migrate:
	${env_vars} && poetry run python manage.py migrate

.PHONY: run
run:
	${env_vars} && poetry run python manage.py runserver 0.0.0.0:8004

.PHONY: run-celery
run-celery:
	${env_vars} && poetry run celery -A config.settings worker -l debug

.PHONY: up
up:
	docker-compose up --force-recreate --build

.PHONY: up-dependencies-only
up-dependencies-only:
	docker-compose up --force-recreate db redis pv cv1 cv2

.PHONY: monitor-pv
monitor-pv:
	docker-compose exec celery_pv celery flower -A config.settings --port=5556

.PHONY: monitor-cv1
monitor-cv1:
	docker-compose exec celery_cv1 celery flower -A config.settings --port=5557

.PHONY: monitor-cv2
monitor-cv2:
	docker-compose exec celery_cv2 celery flower -A config.settings --port=5558

.PHONY: monitor-bank
monitor-bank:
	docker-compose exec celery_bank celery flower -A config.settings --port=5559

.PHONY: monitor-bank-local
monitor-bank-local:
	${env_vars} && poetry run celery flower -A config.settings --address=127.0.0.1
