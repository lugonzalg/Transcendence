COMPOSE=docker compose -f transcendence/docker-compose.yml

.PHONY: all build build-all clean clean-all down fclean restart restart-all stop stop-all

all:
	$(COMPOSE) up -d

build:
	$(COMPOSE) build $(SERVICE)

build-all:
	$(COMPOSE) build

clean:
	bash /manager.sh --clean

cleant-all:
	bash /manager.sh --clean -all

down:
	$(COMPOSE) down

ps:
	$(COMPOSE) ps

restart: stop raise

restart-all: down all

raise: 
	$(COMPOSE) up -d $(SERVICE)

stop:
	$(COMPOSE) stop $(SERVICE)
	$(COMPOSE) rm $(SERVICE)

stop-all: down