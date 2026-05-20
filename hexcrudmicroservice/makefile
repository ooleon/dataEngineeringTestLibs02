.PHONY: build up up-cache up-logs down test logs clean

IMAGE = hex-crud-api
COMPOSE = docker compose

build:
	$(COMPOSE) build --pull

up:
	$(COMPOSE) --profile all up -d

up-cache:
	$(COMPOSE) --profile cache up -d valkey

up-logs:
	$(COMPOSE) --profile logging up -d kafka elasticsearch

down:
	$(COMPOSE) --profile all down -v

test:
	PYTHONPATH=src pytest src/tests -v --tb=short

logs:
	$(COMPOSE) logs -f --tail=50 app

clean:
	docker system prune -f
	docker volume prune -f