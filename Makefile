# simplify the most commonly used docker commands to prevent the
# mistake of using dev args in prod and vice-versa

# config
PROJECT         := molinks
COMPOSE_FILES   := docker-compose.yaml docker-compose.prod.yaml
IMAGE_WEB       := $(PROJECT)-web
IMAGE_DB        := $(PROJECT)-db
IMAGES          := $(IMAGE_WEB) $(IMAGE_DB)
CONTAINER_WEB   := $(IMAGE_WEB)-1
CONTAINER_DB    := $(IMAGE_DB)-1
CONTAINERS      := $(CONTAINER_WEB) $(CONTAINER_DB)
VOLUMES         := $(PROJECT)_postgres-data
PROD_CONTEXT    := prod
STATICFILES_DIR := staticfiles

# get REMOTE_HOST and REMOTE_STATIC from here
-include etc/prod.env

# flags
PROD := $(filter prod,$(MAKECMDGOALS))
MODE := $(if $(PROD),prod,dev)
PROD_ARG1 := $(if $(PROD),--context $(PROD_CONTEXT),)
PROD_ARG2 := $(if $(PROD),$(foreach cf,$(COMPOSE_FILES),-f $(cf)))
BUILD := $(filter build,$(MAKECMDGOALS))
BUILD_ARG := $(if $(BUILD),--build,)
TAIL := $(filter tail,$(MAKECMDGOALS))
TAIL_ARG1 := $(if $(TAIL),,-d)
TAIL_ARG2 := $(if $(TAIL),-f,)

.NOTPARALLEL:
.PHONY: all dev prod build tail
.PHONY: up down ps im clean destroy shell dbshell log init test fakeuser staticfiles

all: up dev
dev: ;@:
prod: ;@:
build: ;@:
tail: ;@:

up:
	docker $(PROD_ARG1) compose $(PROD_ARG2) up $(TAIL_ARG1) $(BUILD_ARG)

down:
	docker $(PROD_ARG1) compose $(PROD_ARG2) down

ps:
	docker $(PROD_ARG1) ps -a

im:
	docker $(PROD_ARG1) image ls -a

clean:
	-docker $(PROD_ARG1) rm $(CONTAINERS)
	-docker $(PROD_ARG1) image rm $(IMAGES)

destroy: clean
	docker $(PROD_ARG1) volume rm $(VOLUMES)

shell:
	docker $(PROD_ARG1) exec -it $(CONTAINER_WEB) bash

dbshell:
	docker $(PROD_ARG1) exec -it $(CONTAINER_DB) psql --username $(PROJECT)

log:
	docker $(PROD_ARG1) logs $(CONTAINER_WEB) $(TAIL_ARG2)

init:
	docker $(PROD_ARG1) exec -it $(CONTAINER_WEB) python manage.py makemigrations $(PROJECT)
	docker $(PROD_ARG1) exec -it $(CONTAINER_WEB) python manage.py migrate
	docker $(PROD_ARG1) exec -it $(CONTAINER_WEB) python manage.py createsuperuser

test:
	docker $(PROD_ARG1) exec -it $(CONTAINER_WEB) python manage.py test $(PROJECT)

fakeuser:
	docker $(PROD_ARG1) exec -it $(CONTAINER_WEB) python manage.py fakeuser

# dev/prod ignored; generates static files from dev then copies them to production server
ifeq ($(strip $(REMOTE_HOST)),)
staticfiles:
	@echo "REMOTE_HOST and REMOTE_STATIC must be setup first; see README.md"
else
staticfiles:
	docker exec -it $(CONTAINER_WEB) python manage.py collectstatic --noinput
	rsync -av $(STATICFILES_DIR)/* $(REMOTE_HOST):$(REMOTE_STATIC)
endif

