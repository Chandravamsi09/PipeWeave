# PipeWeave Build, Test, and Execution Makefile

.PHONY: all build run test lint clean dev docker-build

all: build test

build:
	@echo "Building PipeWeave backend and frontend..."
	python -m pip install -e backend/
	cd frontend && npm install && npm run build

run:
	@echo "Starting PipeWeave Production Server..."
	python main.py serve

dev:
	@echo "Starting PipeWeave in Development Mode..."
	python main.py serve --port 8000 &
	cd frontend && npm run dev

test:
	@echo "Running Automated Pytest & Vitest Suites..."
	PYTHONPATH=backend/src pytest -v tests/

lint:
	@echo "Running Code Formatters and Linters..."
	black --check backend/src
	flake8 backend/src --max-line-length=120 --ignore=E501,W503

docker-build:
	@echo "Building Docker Images..."
	docker compose build

clean:
	@echo "Cleaning cache and build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf dist build *.egg-info
