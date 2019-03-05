#!make
include ./.flaskenv

SHELL := $(shell which bash)
, := ,

# --- Application
app_name := marvin
DOMAIN_NAME ?= localhost
REQUIREMENTS_FILES ?= development

# --- Docker
docker_image := $(app_name)/app:latest
docker_container := $(app_name).app

lambda_image := $(app_name)/app:lambda
lambda_container := $(app_name).lambda

address ?= 127.0.0.1
port ?= 8000
run_port ?= 8001
ngrok_port ?= $(run_port)

docker_exec := docker exec -it $(docker_container)

ifeq (,$(wildcard /.dockerenv))
	exec := $(docker_exec)
endif


help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  build         Build docker image"
	@echo "  up            Run docker container and build if the image does not exist"
	@echo "  restart       Restart docker container"
	@echo "  rm            Remove docker container"
	@echo "  reload        Reload docker container"
	@echo "  logs          View output from docker container"
	@echo "  sh            Run bash shell on the container"
	@echo "  ngrok         Create a tunnel to development server"
	@echo "  run           Run a local development server"
	@echo "  botinfo       Show the current Bot info"
	@echo "  requirements  Install pip requirements from \$$REQUIREMENTS_FILES variable"
	@echo "  lambda        Build λ docker container"
	@echo "  zappa         Run zappa command (usage: make zappa cmd={command})"
	@echo "  test          Run unit tests"
	@echo "  isort         Run isort recursively from your current directory"
	@echo "  coverage      Run unit tests and check the coverage"

build:
	@docker build -t $(docker_image) .

build.if:
	@if [ "$$(docker images -q $(docker_image) 2> /dev/null)" == "" ]; then \
		$(MAKE) -s build; \
	fi

up: build.if
	@docker run $(options) \
		--name $(docker_container) \
		--env-file ./.env \
		--env-file ./.flaskenv \
		-v $(PWD):/marvin \
		-p $(address):$(port):5000 \
		-p $(address):$(run_port):$(FLASK_RUN_PORT) \
		-d $(docker_image)

restart:
	@docker restart $(docker_container)

rm:
	@docker rm -f $(docker_container)

reload: rm up

logs:
	@docker logs -f $(docker_container)

sh:
	@$(docker_exec) /bin/bash

ngrok:
	@ngrok http $(ngrok_port)

run:
	@$(exec) bash -c 'DEFAULT_SUBDOMAIN=$(subdomain) flask run'

botinfo:
	@$(exec) bash -c 'flask botinfo'

requirements:
	@for requirement in $(subst $(,), ,$(REQUIREMENTS_FILES)); do \
		$(exec) pip install -r requirements/$$requirement.txt; \
	done

lambda:
	@docker build -t $(lambda_image) -f lambda/Dockerfile .

zappa:
	@docker run -it --rm \
		--name $(lambda_container) \
		-v $(PWD):/var/task \
		-v ~/.aws:/root/.aws \
		$(lambda_image) zappa $(cmd)

test.requirements:
	@if ! [ $(shell $(exec) which pytest) ]; then \
		REQUIREMENTS_FILES=test $(MAKE) -s requirements; \
	fi

test: test.requirements
	@$(exec) pytest

isort:
	@$(exec) isort -rc .

coverage: test.requirements
	@$(exec) pytest $(options) \
		--verbose \
		--cov=app \
		--cov-report term \
		--cov-report xml

.PHONY: help build build.if up restart rm reload logs sh ngrok run botinfo requirements lambda zappa test.requirements test isort coverage
