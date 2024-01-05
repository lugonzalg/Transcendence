COMPOSE=docker compose -f transcendence/docker-compose.yml

PHONY: all build build-all clean clean-all fclean restart restart-all

clean:
	./manager.sh --clean

cleant-all:
	./manager.sh --clean -all

build:
	$(COMPOSE) build $(SERVICE)

build-all:
	$(COMPOSE) build

restart:
	$(COMPOSE) stop $(SERVICE)
	$(COMPOSE) rm $(SERVICE)
	$(COMPOSE) up -d $(SERVICE)

restart-all:
	$(COMPOSE) down