# Makefile for MultiFlexi MCP Server

.PHONY: help install install-dev test lint format type-check clean build publish run docs

# Default target
help:
	@echo "Available commands:"
	@echo "  install      Install the package"
	@echo "  install-dev  Install package with development dependencies"
	@echo "  test         Run tests"
	@echo "  lint         Run linting (ruff)"
	@echo "  format       Format code (black, isort)"
	@echo "  type-check   Run type checking (mypy)"
	@echo "  clean        Clean build artifacts"
	@echo "  build        Build the package"
	@echo "  publish      Build and upload to PyPI"
	@echo "  publish-test Build and upload to TestPyPI"
	@echo "  run          Run the MCP server"
	@echo "  docs         Generate documentation (if applicable)"

# Installation
install:
	pip install .

install-dev:
	pip install -e ".[dev]"

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=multiflexi_mcp_server --cov-report=html --cov-report=term

# Code quality
lint:
	ruff src/ tests/

format:
	black src/ tests/
	isort src/ tests/

type-check:
	mypy src/

# Clean up
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Build
build: clean
	python -m build

# Publish to PyPI (requires TWINE_USERNAME=__token__ TWINE_PASSWORD=<api-token>)
publish: build
	twine check dist/*
	twine upload dist/*

# Publish to TestPyPI for verification
publish-test: build
	twine check dist/*
	twine upload --repository testpypi dist/*

# Run
run:
	python -m multiflexi_mcp_server.server

# Development server (with auto-reload if available)
dev:
	MULTIFLEXI_DEBUG=true python -m multiflexi_mcp_server.server

# Check all code quality tools
check: format lint type-check test

# Setup development environment
setup-dev: install-dev
	@echo "Development environment set up successfully!"
	@echo "Run 'make check' to verify everything works."

# Release preparation
pre-release: check
	@echo "All checks passed. Ready for release!"

# Docker commands (if Docker is used)
docker-build:
	docker build -t multiflexi-mcp-server .

docker-run:
	docker run -it --rm multiflexi-mcp-server

# Local development with environment variables
dev-env:
	@echo "Setting up development environment variables..."
	@echo "Copy .env.example to .env and customize as needed:"
	@echo "cp .env.example .env"