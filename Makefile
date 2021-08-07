SHELL := /bin/bash
# Just colors
RED=\033[0;31m
GREEN=\033[0;32m
NC=\033[0m

# Network name (default: marvikapi)
NETWORK?=marvikapi
export NETWORK_NAME=$(NETWORK)
NETWORKS=$(shell docker network ls --filter name=^${NETWORK_NAME} --format="{{ .Name }}")

# Compose Files
BASE_FILE=docker/docker-compose.yml
DEV_FILE=docker/docker-compose.dev.yml
PROD_FILE=docker/docker-compose.prod.yml
PROD_COMPOSE_CMD=docker-compose -f $(CURDIR)/$(BASE_FILE) -f $(CURDIR)/$(PROD_FILE)
DEV_COMPOSE_CMD=docker-compose -f $(CURDIR)/$(BASE_FILE) -f $(CURDIR)/$(DEV_FILE)


create_network:
	@if [ -z $(NETWORKS) ]; then \
		printf "${GREEN}Creating network '$(NETWORK_NAME)'${NC}"; \
		docker network create $(NETWORK_NAME); \
	fi;

create_tables:
	$(PROD_COMPOSE_CMD) exec api bash /app/prestart.sh

build: create_network
	$(PROD_COMPOSE_CMD) build

run:
	$(PROD_COMPOSE_CMD) up -d

build_dev: create_network
	$(DEV_COMPOSE_CMD) build --build-arg INSTALL_DEV=true

run_dev:
	$(DEV_COMPOSE_CMD) up -d

stop:
	$(PROD_COMPOSE_CMD) down --remove-orphans

start_project:
	@printf '${GREEN} Installing, creating and activiting virtualenv... ${NC}\n';
	@printf '${GREEN} Installing and configuring poetry... ${NC}\n';
	@printf '${GREEN} Installing project dependencies... ${NC}\n';
	@poetry config virtualenvs.create true --local && poetry config virtualenvs.in-project true --local && poetry install -vv;
	@printf '${GREEN} Configuring pre-commit hooks... ${NC}\n';
	source .venv/bin/activate && pre-commit install
