.PHONY: help clean test install dev-install build

VENV = .venv
BIN = $(VENV)/bin

# Default goal: show help
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@printf "  \033[36m%-15s\033[0m %s\n" "help" "Show this help message"
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) \
		| grep -v '^help:' \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

clean: ## Remove build artifacts and Python cache files
	@echo "Cleaning up..."
	@find . -type d -name "__pycache__" -not -path "*/.venv/*" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -not -path "*/.venv/*" -exec rm -rf {} +
	@rm -rf dist/ build/ src/*.egg-info/ .coverage htmlcov/
	@echo "Cleanup complete."

test: ## Run the test suite using pytest
	$(BIN)/pytest tests/

install: ## Install the package
	$(BIN)/pip install .

dev-install: ## Install the package in editable mode with dev dependencies
	$(BIN)/pip install -e .[dev]

build: clean ## Build source and wheel distributions
	$(BIN)/python -m build