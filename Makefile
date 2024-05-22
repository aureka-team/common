.PHONY: devcontainer-build


devcontainer-build:
	docker compose -f .devcontainer/docker-compose.yml build common-devcontainer


redis-start:
	docker compose -f .devcontainer/docker-compose.yml up -d redis-cache-redis

redis-stop:
	docker compose -f .devcontainer/docker-compose.yml stop redis-cache-redis

redis-flush:
	docker compose -f .devcontainer/docker-compose.yml exec redis-cache-redis redis-cli FLUSHALL
