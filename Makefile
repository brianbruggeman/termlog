# =====================================================================================================
#
# Define help targets with descriptions provided in `##` comments
#
# =====================================================================================================
.PHONY: help printvars

help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

printvars:
	@env | sort
	@$(foreach V,$(sort $(.VARIABLES)), $(if $(filter-out environment% default automatic, $(origin $V)),$(warning $V=$($V) ($(value $V)))))

.DEFAULT_GOAL := help

WORKON_HOME ?= $(HOME)/.virtualenvs
PYTHON_VERSION ?= 3.8
PROJECT_NAME ?= termlog
VENV_PATH ?= $(WORKON_HOME)/$(PROJECT_NAME)
CURRENT_DIR ?=$(shell env | grep -i PWD | cut -d'=' -f2 )

GIT_SHA := $(git rev-parse --short HEAD)
BUILD_DATE := $(date +'%Y%m%d')

POSTGRES_VERSION ?= 11.5
HASH := $(shell git rev-parse --short HEAD 2>/dev/null)
BRANCH := $(shell git branch | grep \* | cut -d ' ' -f2)
PYTHON := $(shell which python$(PYTHON_VERSION))
ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

PACKAGE_VERSION := $(shell cat $(CURRENT_DIR)/pyproject.toml | grep -i "version = \"" | cut -d "\"" -f 2)

# =====================================================================================================
#
# Defined image action targets
#
# See https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html for
# additional details.
#
# =====================================================================================================

$(VENV_PATH)/bin/python:
	$(PYTHON) -m venv $(VENV_PATH)
	$(VENV_PATH)/bin/python -m pip install --upgrade -q pip poetry

venv-path: | $(WORKON_HOME)/$(PROJECT_NAME)/bin/python

venv: venv-path
	$(eval VENV_NAME := $(shell basename $(VENV_PATH)))
	python -m venv $(VENV_PATH)
	. $(VENV_PATH)/bin/activate

install: venv
	pip install .

clean-build: venv
	rm -Rf build dist

install-dev: venv
	poetry install

docs: install-dev  ## Build documentation
	sphinx-build -b html docs/source build/docs

lint: install-dev ## Run lint checking
	mypy .

style: install-dev ## Run style checking
	isort . --check
	black . --check

test: install-dev ## Run tests (fast)
	pytest -ra -vv

release: install-dev  ## Validate for release
	pytest -ra --isort --black --mypy -vv --cache-clear --cov=$(PROJECT_NAME) --cov-report=term-missing --cov-report=term:skip-covered --cov-fail-under=80

publish: clean-build install-dev info release  ## Create and publish release
	poetry publish -r pypi-test --build
	poetry publish

info: venv install printvars ## Show configuration information
	python --version
	pip --version
