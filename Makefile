# =====================================================================================================
#
# Define help targets with descriptions provided in `##` comments
#
# =====================================================================================================
.DEFAULT_GOAL := all

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir := $(dir $(mkfile_path))
OSUPPER = $(shell uname -s 2>/dev/null | tr [:lower:] [:upper:])
DARWIN = $(strip $(findstring DARWIN, $(OSUPPER)))
VARS_OLD := $(.VARIABLES)
PWD := $(shell printenv | grep PWD | cut -d= -f2)
SHELL1 := $(shell ps $$$$ | tail -n 1 | awk '{print $$5}')
SHELL2 := $(shell echo $$SHELL)
ifeq ($(SHELL2),)
ifeq ($(SHELL1),/bin/sh)
USER_SHELL ?= /bin/bash
else
USER_SHELL ?= $(SHELL1)
endif
else
USER_SHELL ?= $(SHELL2)
endif

# ----------------------------------------------------------------------
# Dotenv load
DOTENV_FILE ?= ./.env
ENV_FILE ?= $(DOTENV_FILE)
ifneq (,$(wildcard $(ENV_FILE)))
	include $(ENV_FILE)
	export $(shell grep -v '^\s*\#.*' $(ENV_FILE) | grep -v '^\s*$$' | sed 's/=.*//' | sed 's/^\s*export//' )
endif

WORKON_HOME ?= $(HOME)/.virtualenvs
PROJECT_NAME ?= termlog
POETRY_VIRTUALENVS_PATH ?= $(WORKON_HOME)
VENV_PATH ?= $(WORKON_HOME)/$(PROJECT_NAME)
CURRENT_DIR ?=$(shell env | grep -i PWD | cut -d'=' -f2 )

GIT_SHA := $(git rev-parse --short HEAD)
BUILD_DATE := $(date +'%Y%m%d')

PYTHON_VERSION ?= 3.8
HASH := $(shell git rev-parse --short HEAD 2>/dev/null || echo "")
BRANCH := $(shell git branch | grep \* | cut -d ' ' -f2 || echo "")

SYSTEM_PYTHON ?= $(shell which python$(PYTHON_VERSION))

VENV_BIN_PATH := $(VENV_PATH)/bin
ACTIVATE := $(VENV_BIN_PATH)/activate
BLACK := $(VENV_BIN_PATH)/black
ISORT := $(VENV_BIN_PATH)/isort
MYPY := $(VENV_BIN_PATH)/mypy
PIP := $(VENV_BIN_PATH)/pip
POETRY := $(VENV_BIN_PATH)/poetry
PYTEST := $(VENV_BIN_PATH)/pytest
PYTHON := $(VENV_BIN_PATH)/python
SPHINX_BUILD := $(VENV_BIN_PATH)/sphinx-build

ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
DEFAULT_PKG_VERSION ?= $(shell cat pyproject.toml | grep -i "^version = " | cut -d\' -f2 | cut -d' ' -f3 | sed "s/'//g" | sed 's/"//g')
ifneq "" "$(BITBUCKET_TAG)"
PKG_VERSION ?= $(BITBUCKET_TAG)
else
PKG_VERSION ?= $(DEFAULT_PKG_VERSION)
endif


# =====================================================================================================
#
# Defined image action targets
#
# See https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html for
# additional details.
#
# =====================================================================================================
all:: fmt test

clean:: ## Clean build artifacts
	rm -Rf build dist .mypy_cache .pytest_cache *.egg-info .venv $(VENV_PATH)

docs:: | $(SPHINX_BUILD) ## Build documentation
	$(SPHINX_BUILD) -b html docs/source build/docs

fmt:: | $(VENV_PATH) $(POETRY) $(ISORT) $(BLACK)
	$(BLACK) .
	$(ISORT) .

help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

lint:: | $(MYPY) ## Run lint checking
	$(MYPY) .

info:: | $(ACTIVATE) printvars ## Show configuration information
	. $(ACTIVATE) && python --version
	. $(ACTIVATE) && pip --version
	$(POETRY) env info

install:: | $(POETRY)
	$(POETRY) install

printvars:
	@$(foreach V,$(sort $(.VARIABLES)), $(if $(filter-out environment% default automatic, $(origin $V)),$(warning $V=$($V) ($(value $V)))))
	@env | sort

publish: $(ACTIVATE) $(POETRY) clean venv-build install info release  ## Create and publish release
	$(POETRY) publish -r pypi-test --build
	$(POETRY) publish

release: install  ## Validate for release
	$(PYTEST) -ra --isort --black --mypy -vv --cache-clear --cov=$(PROJECT_NAME) --cov-report=term-missing --cov-report=term:skip-covered --cov-fail-under=80

style:: | $(BLACK) $(ISORT)  ## Run style checking
	$(BLACK) . --check
	$(ISORT) . --check

test:: install ## Run tests (fast)
	$(PYTEST) -ra -vv

update: $(POETRY)
	$(POETRY) update

venv:: | $(VENV_PYTHON)  ## Shells into virtual environment
	@echo "Activating virtualenv under '$(VENV_PATH)' using shell '$(USER_SHELL)':" && $(USER_SHELL) --login -c ". $(VENV_PATH)/bin/activate && $(USER_SHELL) -i"
	@echo "Exited virtualenv"

venv-build:: | $(POETRY)

venv-clean::
	rm -Rf $(VENV_PATH)

venv-rebuild:: venv-clean venv-build

# ----------------------------------------------------------------------
requirements.txt: | $(POETRY)  ## Generate requirements.txt
	$(POETRY) export -f requirements.txt --output requirements.txt

requirements-dev.txt: | $(POETRY)  ## Generate requirements.txt
	$(POETRY) export --dev -f requirements.txt --output requirements-dev.txt

setup.py: | $(POETRY)  ## Creates a setup.py for local development
	$(POETRY) build -f sdist
	tar xvzf dist/termlog-$(DEFAULT_PKG_VERSION).tar.gz --strip-components=1 -C . termlog-$(DEFAULT_PKG_VERSION)/setup.py

$(ACTIVATE):
	@echo "Creating venv under ${VENV_PATH}"
	$(SYSTEM_PYTHON) -m venv $(VENV_PATH)

$(POETRY): | $(ACTIVATE)
	@echo "Setting up venv with required packages"
	$(PYTHON) -m pip install --upgrade -q pip poetry
	. $(ACTIVATE) && $(POETRY) config virtualenvs.create false
	. $(ACTIVATE) && $(POETRY) config virtualenvs.in-project false
	. $(ACTIVATE) && $(POETRY) config virtualenvs.path $(WORKON_HOME)
	. $(ACTIVATE) && $(POETRY) config cache-dir $(WORKON_HOME)

$(ISORT): | $(ACTIVATE) $(POETRY)
	. $(ACTIVATE) && $(POETRY) install

$(BLACK): | $(ACTIVATE) $(POETRY)
	. $(ACTIVATE) && $(POETRY) install

$(PYTEST): | $(ACTIVATE) $(POETRY)
	. $(ACTIVATE) && $(POETRY) install

$(MYPY): | $(ACTIVATE) $(POETRY)
	. $(ACTIVATE) && $(POETRY) install

$(SPHINX_BUILD): | $(ACTIVATE) $(POETRY)
	. $(ACTIVATE) && $(POETRY) install