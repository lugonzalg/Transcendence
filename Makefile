COMPOSE=docker compose -f docker-compose.yml

.PHONY: all build build-all clean clean-all down fclean follow follow-all ps restart restart-all stop stop-all

all:
	make -C ./dependencies
	make -C ./develop

vault:
	$(COMPOSE) up -d vault
	@sleep 1
	$(COMPOSE) exec vault /docker-entrypoint/init.sh sh

build:
	$(COMPOSE) build $(SERVICE)

build-all:
	$(COMPOSE) build

clean:
	bash Tools/manager.sh --clean

cleant-all:
	bash Tools/manager.sh --clean -all

down:
	$(COMPOSE) down

follow:
	$(COMPOSE) logs --follow --tail 1000 $(SERVICE)

follow-all:
	$(COMPOSE) logs --follow --tail 1000

migrate:
	$(COMPOSE) exec $(SERVICE) python /app/manage.py makemigrations $(SERVICE)
	$(COMPOSE) exec $(SERVICE) python /app/manage.py migrate

migrate-all:
	@echo "hehe"

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

psql:
	$(COMPOSE) exec postgres psql -U Astro98 transcendence

migrations:
	cd Tools && python3 main_cleaner.py
