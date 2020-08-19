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
PROJECT_NAME ?= termlog
POETRY_VIRTUALENVS_PATH ?= $(WORKON_HOME)
VENV_PATH ?= $(WORKON_HOME)/$(PROJECT_NAME)
CURRENT_DIR ?=$(shell env | grep -i PWD | cut -d'=' -f2 )

GIT_SHA := $(git rev-parse --short HEAD)
BUILD_DATE := $(date +'%Y%m%d')

POSTGRES_VERSION ?= 11.5
HASH := $(shell git rev-parse --short HEAD 2>/dev/null)
BRANCH := $(shell git branch | grep \* | cut -d ' ' -f2)

SYSTEM_PYTHON := python3

VENV_BIN_PATH := $(VENV_PATH)/bin
PIP := $(VENV_BIN_PATH)/poetry
POETRY := $(VENV_BIN_PATH)/poetry
ACTIVATE := $(VENV_BIN_PATH)/activate
PYTHON := $(VENV_BIN_PATH)/python
PYTEST := $(VENV_BIN_PATH)/pytest
MYPY := $(VENV_BIN_PATH)/mypy
ISORT := $(VENV_BIN_PATH)/isort
BLACK := $(VENV_BIN_PATH)/black
SPHINX_BUILD := $(VENV_BIN_PATH)/sphinx-build
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

$(ACTIVATE):
	@echo "Creating venv under ${VENV_PATH}"
	$(SYSTEM_PYTHON) -m venv $(VENV_PATH)

$(POETRY): | $(ACTIVATE)
	@echo "Setting up venv with required packages"
	$(PYTHON) -m pip install --upgrade -q pip poetry
	. $(ACTIVATE) && $(POETRY) env use $(VENV_BIN_PATH)/python
	. $(ACTIVATE) && $(POETRY) config virtualenvs.create false

$(ISORT): | $(ACTIVATE) $(POETRY)
	$(POETRY) run pip install isort

$(BLACK): | $(ACTIVATE) $(POETRY)
	$(POETRY) env info
	$(POETRY) run pip install black

$(PYTEST): | $(ACTIVATE) $(POETRY)
	$(POETRY) run pip install pytest

$(MYPY): | $(ACTIVATE) $(POETRY)
	$(POETRY) run pip install mypy

$(SPHINX_BUILD): | $(ACTIVATE) $(POETRY)
	$(POETRY) run pip install sphinx

venv-path: | $(ACTIVATE) $(POETRY)

venv: venv-path

install: venv
	$(POETRY) install

clean-venv:
	rm -Rf $(VENV_PATH)

clean-dev:
	rm -Rf .mypy_cache .pytest_cache *.egg-info .venv

clean-build:
	rm -Rf build dist

clean: clean-venv clean-build clean-dev

docs: $(SPHINX_BUILD) install ## Build documentation
	$(SPHINX_BUILD) -b html docs/source build/docs

lint: $(MYPY) ## Run lint checking
	$(MYPY) .

black: $(BLACK) ## Run black formatting
	$(BLACK) . --check

isort: $(ISORT) ## Run isort formatting
	$(ISORT) . --check

style: install black isort  ## Run style checking

test: install ## Run tests (fast)
	$(PYTEST) -ra -vv

release: install  ## Validate for release
	$(PYTEST) -ra --isort --black --mypy -vv --cache-clear --cov=$(PROJECT_NAME) --cov-report=term-missing --cov-report=term:skip-covered --cov-fail-under=80

publish: $(ACTIVATE) $(POETRY) clean-build install info release  ## Create and publish release
	$(POETRY) publish -r pypi-test --build
	$(POETRY) publish

info: $(ACTIVATE) install printvars ## Show configuration information
	$(ACTIVATE) && python --version
	$(ACTIVATE) && pip --version
