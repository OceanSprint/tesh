# Convenience makefile to build the dev env and run common commands
PYTHON ?= python3.11


.PHONY: all
all: tests

# Testing and linting targets
all = false

.PHONY: lint
lint:
# 1. get all unstaged modified files
# 2. get all staged modified files
# 3. get all untracked files
# 4. run pre-commit checks on them
ifeq ($(all),true)
	@pre-commit run --all-files
else
	@{ git diff --name-only ./; git diff --name-only --staged ./;git ls-files --other --exclude-standard; } \
		| sort -u | uniq | xargs pre-commit run --hook-stage push --files
endif

.PHONY: type
type: types

.PHONY: types
types: .
	@mypy src/tesh
	@typecov 100 ./typecov/linecount.txt


# anything, in regex-speak
filter = "."

# additional arguments for pytest
full_suite = "false"
ifeq ($(filter),".")
	full_suite = "true"
endif
ifdef path
	full_suite = "false"
endif
args = ""
pytest_args = -k $(filter) $(args)
ifeq ($(args),"")
	pytest_args = -k $(filter)
endif
verbosity = ""
ifeq ($(full_suite),"false")
	verbosity = -vv
endif
full_suite_args = ""
ifeq ($(full_suite),"true")
	full_suite_args = --junitxml junit.xml --durations 10 --cov=tesh --cov-branch --cov-report html --cov-report xml:cov.xml --cov-report term-missing --cov-fail-under=100
endif


.PHONY: unit
unit:
ifndef path
	@pytest src/tesh $(verbosity) $(full_suite_args) $(pytest_args)
else
	@pytest $(path)
endif

.PHONY: tesh
tesh:
	@tesh *.md

.PHONY: examples
examples:
	@echo "You need nix-shell to run 'make examples'"

.PHONY: test
test: tests

.PHONY: tests
tests:
	@make lint all=true
	@make types
	@make unit
	@make tesh
	@make examples
