.PHONY: devcontainer-build


devcontainer-build:
	docker compose -f .devcontainer/docker-compose.yml build common-devcontainer


redis-start:
	docker compose -f .devcontainer/docker-compose.yml up -d common-redis

redis-stop:
	docker compose -f .devcontainer/docker-compose.yml stop common-redis

redis-flush:
	docker compose -f .devcontainer/docker-compose.yml exec common-redis redis-cli FLUSHALL

redis-restart: redis-stop redis-start
