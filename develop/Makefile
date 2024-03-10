COMPOSE=docker compose -f docker-compose.yml

.PHONY: all clean fclean re

all:
	$(COMPOSE) up -d $(SER)

build:
	$(COMPOSE) build $(SER)

clean: down rm
	VOLUMES=$$(docker volume ls -q | awk '/^core/')
	
	ifeq ($(VOLUMES))
	docker volume rm $$(docker volume ls -q | awk '/^core/')
	endif

down:
	$(COMPOSE) down $(SER)

rm:
	$(COMPOSE) rm $(SER)

ps:
	$(COMPOSE) ps $(SER)

stop:
	$(COMPOSE) stop $(SER)

live:
	$(COMPOSE) up

follow:
	$(COMPOSE) logs --follow --tail 200 $(SER)