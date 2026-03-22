# Makefile - работает на Mac и Linux (и Windows с make)

.PHONY: help install run docker-up docker-down dev

help:
	@echo "📋 Available commands:"
	@echo "  make install     - install dependencies"
	@echo "  make run         - run application"
	@echo "  make docker-up   - start Docker containers"
	@echo "  make docker-down - stop Docker containers"
	@echo "  make dev         - run everything"

venv:
	python -m venv venv
	@echo 'To activate venv: venv\scripts\activate'

install:
	pip install -r requirements.txt

run:
	uvicorn src.main:app --reload

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

dev: docker-up run
