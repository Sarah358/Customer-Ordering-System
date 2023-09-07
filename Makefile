ifneq (,$(wildcard ./.env))
include .env
export
ENV_FILE_PARAM = --env-file .env

endif
pre-commit:
	pre-commit run --all-files
build:
	docker compose up --build -d --remove-orphans

up:
	docker compose up -d

down:
	docker compose down
