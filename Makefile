APP_NAME = atlas
LOCAL_PLATFORM = linux/$(shell docker info --format '{{.Architecture}}' | sed 's/x86_64/amd64/;s/aarch64/arm64/')
PLATFORMS = linux/amd64,linux/arm64
REGISTRY ?= my-registry
TAG ?= latest

## Load environment vars
.PHONY: load-env
load-env:
	export $(shell sed 's/=.*//' $(.env))


## Create a multi-arch buildx builder (run once)
.PHONY: buildx.setup
buildx.setup:
	docker buildx create --name multiarch --driver docker-container --use 2>/dev/null || docker buildx use multiarch


## Install dependencies
.PHONY: install
install:
	poetry install
	pre-commit install


## Commands local
PHONY: local.run
local.run:
	uvicorn src.presentation.api.main:api --host 0.0.0.0 --port 8080 --reload

PHONY: local.test
local.test:
	run pytest --cov=code tests/code --cov-report=term

PHONY: local.lock
local.lock:
	poetry lock --no-update


## Build images
.PHONY: build.deployment
build.deployment:
	docker buildx build --platform $(LOCAL_PLATFORM) --load -t $(APP_NAME)-deployment . --target final

.PHONY: build.deployment.push
build.deployment.push: buildx.setup
	docker buildx build --platform $(PLATFORMS) --push -t $(REGISTRY)/$(APP_NAME):$(TAG) . --target final

.PHONY: build.unit-tests
build.unit-tests:
	docker buildx build --platform $(LOCAL_PLATFORM) --load -t $(APP_NAME)-tests . --target tests

.PHONY: build.e2e-tests
build.e2e-tests:
	docker compose down --volumes
	docker buildx build --platform $(LOCAL_PLATFORM) --load -t $(APP_NAME)-tests . --target tests

.PHONY: build.coverage-report
build.coverage-report:
	docker compose down --volumes
	docker buildx build --platform $(LOCAL_PLATFORM) --load -t $(APP_NAME)-tests . --target tests


## Delete images
.PHONY: rmi.deployment
rmi.deployment:
	docker rmi -f $(APP_NAME)-deployment

.PHONY: rmi.linter
rmi.linter:
	docker rmi -f $(APP_NAME)-linter

.PHONY: rmi.unit-tests
rmi.unit-tests:
	docker rmi -f $(APP_NAME)-unit-tests

.PHONY: rmi.e2e-tests
rmi.e2e-tests:
	docker rmi -f $(APP_NAME)-e2e-tests

.PHONY: rmi.coverage-report
rmi.coverage-report:
	docker rmi -f $(APP_NAME)-coverage-report


## Run containers
.PHONY: run.deployment
run.deployment:
	docker compose up -d api consumer

.PHONY: run.unit-tests
run.unit-tests:
	docker compose down --volumes --remove-orphans
	DOCKER_DEFAULT_PLATFORM=$(LOCAL_PLATFORM) docker compose run --rm unit-tests
	docker compose down --volumes --remove-orphans

.PHONY: run.e2e-tests
run.e2e-tests:
	docker compose down --volumes --remove-orphans
	DOCKER_DEFAULT_PLATFORM=$(LOCAL_PLATFORM) docker compose run --rm e2e-tests
	docker compose down --volumes --remove-orphans

.PHONY: run.coverage-report
run.coverage-report:
	make run.unit-tests
	make run.e2e-tests
	docker compose down --volumes --remove-orphans
	DOCKER_DEFAULT_PLATFORM=$(LOCAL_PLATFORM) docker compose run --rm coverage-report
	docker compose down --volumes --remove-orphans

## Stop containers
.PHONY: stop.all
stop.all:
	docker compose stop


## Migrations
.PHONY: makemigrations
makemigrations:
	docker exec -i $(APP_NAME)-api alembic revision --autogenerate -m "$(name)"

.PHONY: migrate
migrate:
	docker exec -i $(APP_NAME)-api alembic upgrade head


## Show container logs.
.PHONY: logs.api
logs.api:
	docker logs --tail 100 -f ${APP_NAME}-api

.PHONY: logs.consumer
logs.consumer:
	docker logs --tail 100 -f ${APP_NAME}-consumer
