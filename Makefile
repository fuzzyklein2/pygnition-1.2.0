# Fully working lightweight Makefile for Linux/macOS using custom Python
# Designed for project root layout: pyproject.toml + setup.py in the root

PYTHON := /home/fuzzy/python-3.13.2/bin/python3  # <-- your custom Python
PROJECT_DIR := $(notdir $(CURDIR))
MAIN_VENV := .venv
MAIN_PYTHON := $(MAIN_VENV)/bin/python

# Default target: setup dev environment
.PHONY: dev
dev: bootstrap install_main_requirements install_main_package setup_examples
	@echo "Development environment ready."

# Create main venv if missing
$(MAIN_VENV):
	@echo "Creating main virtual environment at $(MAIN_VENV)..."
	$(PYTHON) -m venv $(MAIN_VENV)

# Bootstrap pip in main venv if missing
.PHONY: bootstrap
bootstrap: $(MAIN_VENV)
	@echo "Bootstrapping pip in main venv..."
	@$(MAIN_PYTHON) -m pip --version >/dev/null 2>&1 || \
		($(MAIN_PYTHON) -m ensurepip --upgrade 2>/dev/null || \
		 curl -sS https://bootstrap.pypa.io/get-pip.py | $(MAIN_PYTHON))
	$(MAIN_PYTHON) -m pip install --upgrade pip

# Install main project dependencies
.PHONY: install_main_requirements
install_main_requirements: bootstrap
	@echo "Installing main project dependencies..."
	@if [ -f requirements.txt ]; then \
	    $(MAIN_PYTHON) -m pip install -r requirements.txt; \
	fi

# Install main package editable from project root
.PHONY: install_main_package
install_main_package: bootstrap
	@echo "Installing main package in editable mode..."
	$(MAIN_PYTHON) -m pip install -e .

# Setup per-example venvs
.PHONY: setup_examples
setup_examples: bootstrap
	@for example in docs/examples/*/ ; do \
		echo "Setting up venv for $$example"; \
		if [ ! -d "$$example/.venv" ]; then \
			$(PYTHON) -m venv "$$example/.venv"; \
		fi; \
		EX_PY="$$example/.venv/bin/python"; \
		EX_PIP="$$example/.venv/bin/pip"; \
		# Bootstrap pip in example venv if missing \
		$$EX_PY -m pip --version >/dev/null 2>&1 || \
			($$EX_PY -m ensurepip --upgrade 2>/dev/null || \
			 curl -sS https://bootstrap.pypa.io/get-pip.py | $$EX_PY); \
		$$EX_PY -m pip install --upgrade pip; \
		# Generate stub requirements.in if missing \
		if [ ! -f "$$example/requirements.in" ] && [ ! -f "$$example/requirements.txt" ]; then \
			echo "# Auto-generated empty requirements" > "$$example/requirements.in"; \
		fi; \
		# Install dependencies \
		if [ -f "$$example/requirements.in" ]; then \
			$$EX_PIP install -r "$$example/requirements.in"; \
		elif [ -f "$$example/requirements.txt" ]; then \
			$$EX_PIP install -r "$$example/requirements.txt"; \
		fi; \
		# Install main package editable from project root \
		$$EX_PY -m pip install -e .; \
	done

# Run tests
.PHONY: test
test: dev
	@echo "Running tests..."
	$(MAIN_PYTHON) -m pytest tests

# Clean main venv
.PHONY: clean
clean:
	@echo "Removing main virtual environment..."
	rm -rf $(MAIN_VENV)
