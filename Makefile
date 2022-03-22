# Copyright 2020 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
PWD:=$(shell pwd)

DOCKER_CONTAINER:=app
DOCKER_COMPOSE:=docker-compose -f $(PWD)/docker-compose.yaml

.PHONY: all

all: clean
	$(DOCKER_COMPOSE) stop
	$(DOCKER_COMPOSE) up --build --no-start
	$(DOCKER_COMPOSE) up -d "${DOCKER_CONTAINER}"
	$(DOCKER_COMPOSE) run "${DOCKER_CONTAINER}" make all
	$(DOCKER_COMPOSE) stop

clean: 
	$(DOCKER_COMPOSE) stop
	docker-compose down
	docker rm -f $(docker ps -a -q)
	docker volume rm $(docker volume ls -q)
